# waterbodies_app/urls.py
from django.urls import path
from .views import index
from .views import admin_login, admin_dashboard
from django.contrib.auth.views import LogoutView

from .views import delete_water_body_confirmation

from . import views
from .views import(
    index,
    admin_login,
    admin_dashboard,
    Logoutview,
    water_body_list,
    add_water_body,
    get_water_body_data, 
    get_taluk_data,
    get_block_data,
    tableau_visualization,
    
    water_body_details,
    
    
    
    )
from .views import field_worker_list
from .views import register_field_worker
from .views import change_password
from .views import volunteer_form
from .views import field_worker_login
from .views import waterbody_lists
from .views import volunteers_list
from .views import user_dashboard
urlpatterns = [
    path('', index, name='index'),
     path('change-password/', change_password, name='change_password'),
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('logout/', views.Logoutview, name='logout'), 
    path('water-bodies/', water_body_list, name='waterbody-list'),
    path('add-water-body/', add_water_body, name='add-water-body'),
    path('api/get-water-body-data/', get_water_body_data, name='get-water-body-data'),
    
    path('delete-water-body-confirmation/<int:waterbody_id>/', delete_water_body_confirmation, name='delete_water_body_confirmation'),
    path('tableau-visualization/', tableau_visualization, name='tableau_visualization'),

     path('volunteer/', volunteer_form, name='volunteer_form'),
     path('volunteers/', volunteers_list, name='volunteers_list'),
     path('field-workers/', field_worker_list, name='field_worker_list'),
    path('water_body_details/<int:water_body_id>/', water_body_details, name='water_body_details'),

     path('waterbody-lists/', waterbody_lists, name='waterbody_lists'),

   
   path('api/get-taluk-data/', get_taluk_data, name='get-taluk-data'),
   path('api/get-block-data/', get_block_data, name='get_block_data'),
    path('field-worker-login/', field_worker_login, name='field_worker_login'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
   path('register/field-worker/', register_field_worker, name='register_field_worker'),



    # Add more URL patterns for your app...
]
