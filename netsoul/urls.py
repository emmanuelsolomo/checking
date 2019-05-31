#from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.authtoken import views as rest_framework_views

from . import views

urlpatterns = [
  # /netsoul
  path('', views.home, name='home'),
  path('signin', views.sign_in, name='signin'),
  path('callback', views.callback, name='callback'),
  path('signout', views.sign_out, name='signout'),
  path('dashboard', views.dashboard,  name='dashboard'),
  path('nslog', views.nslog,  name='nslog'),
  path('dashboardlogs', views.dashboardlogs,  name='dashboardlogs'),
  path('userdashboardlogs/<email>', views.userdashboardlogs,  name='userdashboardlogs'),
  path('activity', views.getActivity,  name='activity'),
  path('getUserGroups', views.getUserGroups,  name='getUserGroups'),
  path('userInfo', views.getUserInfo,  name='userInfo'),
  path('logs', views.NsLogView.as_view(), name='logs'),
  path('get_auth_token', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]+ static(settings.NODE_MODULE_URL, document_root=settings.NODE_MODULE_ROOT) + static(settings.JS_URL, document_root=settings.JS_ROOT) + static(settings.VIEWS_URL, document_root=settings.VIEWS_ROOT) + static(settings.IMG_URL, document_root=settings.IMG_ROOT) + static(settings.CSS_URL, document_root=settings.CSS_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



