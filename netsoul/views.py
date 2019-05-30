from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from netsoul.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token, _auth_completed, _logout_completed, is_logged_in
from netsoul.graph_helper import get_user, get_calendar_events
import dateutil.parser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import NsLog, O365User
from .serializers import NsLogSerializer, O365UserSerializer
import datetime
import pandas as pd
from datetime import timedelta
#from django.utils import timezone
from checking.celery import app
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from .logs import LogManager
from .dashboard import DashBoardManager
from rest_framework import status
import pytz


class NsLogView(APIView):
    permission_classes = (IsAuthenticated,) 

    def post(self, request, format=None):
        print(request.user)
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
        logMgr = LogManager(str(request.user), ip)
        logMgr.updateNsLog(originWeb=False)
        logMgr.updateActivity()
        return Response(dict(msg='Nslog table updated',status='Success'), status=status.HTTP_201_CREATED)
            
def check_timedelta(data, time1, time2, ip):  
  date_time2_obj = datetime.datetime.strptime(time2.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')
  date_time1_obj = datetime.datetime.strptime(time1.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')  
  time_difference =  date_time1_obj - date_time2_obj

  time_difference_in_minutes = time_difference / timedelta(minutes=1)
  shift_array = []
  if (time_difference_in_minutes > 15):    
    shift = 1
    new_row = date_time2_obj    
    while shift < (time_difference_in_minutes / 5):      
      new_row = new_row + timedelta(minutes=5)
      log = dict(user=data['user'],date=data['date'],timestamp=new_row.strftime('%Y-%m-%dT%H:%M:%S%z'),last_signin=False,ip=ip,active=False)
      shift_array.append(log)
      shift = shift + 1
    
  return shift_array

def find_inactivy(data, ip):
  current = 0
  while current < len(data):
    if current > 0:
      shift_array = check_timedelta(data[current], data[current]['timestamp'], data[current - 1]['timestamp'], ip)
      if (len(shift_array) > 0):
        cpt = 0 
        index = current
        while(cpt < len(shift_array)):
          data.insert(index, shift_array[cpt])
          cpt = cpt + 1
          index = index + 1          
    current += 1
  return data

def initialize_context(request):
  context = {}

  # Check for any errors in the session
  error = request.session.pop('flash_error', None)

  if error != None:
    context['errors'] = []
    context['errors'].append(error)

  # Check for user in the session
  context['user'] = request.session.get('user', {'is_authenticated': False})
  return context

def home(request):
  context = initialize_context(request)
  if 'user' in request.session:
    return HttpResponseRedirect(reverse('dashboard'))

  return render(request, 'netsoul/home.html', context)
  # Temporary!
  #return HttpResponse("Welcome to the netsoul.")


def sign_in(request):
  # Get the sign-in URL
  sign_in_url, state = get_sign_in_url()
  # Save the expected state so we can validate in the callback
  request.session['auth_state'] = state
  # Redirect to the Azure sign-in page
  return HttpResponseRedirect(sign_in_url)

def callback(request):
  # Get the state saved in session
  expected_state = request.session.pop('auth_state', '')
  # Make the token request
  token = get_token_from_code(request.get_full_path(), expected_state)

  # Get the user's profile
  user = get_user(token)

  # Save token and user
  store_token(request, token)
  store_user(request, user)
  _auth_completed(request, user)
  timezone = pytz.timezone("Africa/Porto-Novo")
  log_time = timezone.localize(datetime.datetime.now())
  logtime = log_time.strftime('%Y-%m-%dT%H:%M:%S%z')

  #log_time = datetime.datetime.now()
  #logtime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')
  ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
  email = user=request.session['user']['email']
  data = dict(user=request.session['user']['email'],timestamp=logtime,last_signin=logtime, ip=ip,active=True)
  serializer = NsLogSerializer(data=data)
  if serializer.is_valid():
    serializer.save()
    UserActivity = O365User.objects.get(email=email)
    UserActivity.active = True
    UserActivity.last_activity = log_time
    UserActivity.last_seen = "less than a minute ago"
    UserActivity.save()
  return HttpResponseRedirect(reverse('dashboard'))

def sign_out(request):
  # Clear out the user and token
  _logout_completed(request)
  remove_user_and_token(request)

  return HttpResponseRedirect(reverse('home'))

def check_o365_verification(user):
    return True 

def check_o365(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        check_o365_verification,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def dashboard(request):
  context = initialize_context(request)

  data = is_logged_in(request)
  if data['status'] == False:
    return HttpResponseRedirect(reverse('home'))

  token = get_token(request)

  return render(request, 'netsoul/dashboard.html', context)


@csrf_exempt
def nslog(request):
    """
    Return all nslog for a given user and save a log
    """
    if request.method == 'GET':
        print(request.user_agent.browser)
        print(request.user_agent.browser.family)
        print(request.user_agent.browser.version)        
        print(request.user_agent.os)
        print(request.user_agent.os.family)
        print(request.user_agent.os.version)
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
        if not 'user' in request.session:
          remove_user_and_token(request)
          return HttpResponseRedirect(reverse('home'))
        else:
          user = request.session['user']['email']
          logMgr = LogManager(user, ip)
          if  logMgr.nbLog > 0: 
            logMgr.updateNsLog()
            logMgr.updateActivity()
            return HttpResponseRedirect(reverse('home'))
          remove_user_and_token(request)
          return HttpResponseRedirect(reverse('home'))        

@csrf_exempt
def dashboardlogs(request):
    """
    Return all nslog for a given user 
    """
    if request.method == 'GET':
      if 'user' not in request.session:
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))        
      user = request.session['user']['email']
      ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
      logMgr = LogManager(user, ip)
      if  logMgr.nbLog == 0: 
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))
      dshLogs = DashBoardManager(user, ip)
      logMgr.updateActivity()  
      return JsonResponse(dshLogs.dashboardData, safe=False)


@csrf_exempt
def userdashboardlogs(request,email):
    """
    Return all nslog for a given user 
    """
    if request.method == 'GET':
      if 'user' not in request.session:
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))
      ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[-1].strip()
      logMgr = LogManager(email, ip)
      if  logMgr.nbLog == 0: 
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))
      dshLogs = DashBoardManager(email, ip)
      logMgr.updateActivity()  
      return JsonResponse(dshLogs.dashboardData, safe=False)

@csrf_exempt
def getActivity(request):
    """
    Return all nslog for a given user 
    """
    if request.method == 'GET':
      if 'user' not in request.session:
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))        
      activity = O365User.objects.all()
      serializer = O365UserSerializer(activity, many=True)
      activityData = dict(data=serializer.data,email=request.session['user']['email'])
      return JsonResponse(activityData, safe=False)

@csrf_exempt
def getUserGroups(request):
    """
    Return all nslog for a given user 
    """
    if request.method == 'GET':
      if 'user' not in request.session:
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))        
      groups = O365User.objects.all()
      serializer = O365UserSerializer(groups, many=True)
      tek1 = 0
      tek2 = 0
      tek3 = 0
      staff = 0
      for user in serializer.data:
        if (user['group'] == 'STAFF' and user['active'] == True):
          staff = staff + 1
        if (user['group'] == 'Tek1' and user['active'] == True):
          tek1 = tek1 + 1
        if (user['group'] == 'Tek2' and user['active'] == True):
          tek2 = tek2 + 1
        if (user['group'] == 'Tek3' and user['active'] == True):
          tek3 = tek3
      return JsonResponse(dict(staff=staff,tek1=tek1,tek2=tek2,tek3=tek3), safe=False)


@csrf_exempt
def getUserInfo(request):
    """
    Return all nslog for a given user 
    """
    if request.method == 'GET':
      if 'user' not in request.session:
        sign_out(request)
        return HttpResponseRedirect(reverse('home'))        
      user = O365User.objects.filter(email=request.session['user']['email'])
      UserSerializer = O365UserSerializer(user, many=True)
      return JsonResponse(UserSerializer.data, safe=False)

