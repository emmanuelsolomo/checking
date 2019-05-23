#from django.contrib import admin
from django.urls import path, include


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
#  path('admin/', admin.site.urls),
]


