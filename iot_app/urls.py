# iot_app/urls.py
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logs/', views.view_logs, name='view_logs'),
    path('home/', views.home, name='home'),
    path('update/', views.update, name='update'),
    path('status/', views.status, name='status'),
    path('get_status/', views.get_status, name='get_status'),
    path('user_login/', views.user_login_view, name='user_login'),
    path('admin_login/', views.admin_login_view, name='admin_login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle_debug_mode/', views.toggle_debug_mode, name='toggle_debug_mode'),
    path('send_reload_message/', views.send_reload_message, name='send_reload_message'),
    path('debug/', views.debug, name='debug'),

]