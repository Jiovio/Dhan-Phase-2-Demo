# waterbodies_app/urls.py
from django.conf import settings
from django.conf.urls.static import static
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
    dashboardanalytics,
    
    water_body_details,
    
    
    
    )
#from .views import field_worker_list
#from .views import register_field_worker
from .views import change_password
from .views import volunteer_form
#from .views import field_worker_login
from .views import waterbody_lists
from .views import volunteers_list
from .views import user_dashboard
from .views import custom_login_view
from .views import register_view
from .views import user_list_view
from .views import pond_list
from .views import fetch_water_spread_data
from .views import upload_kml
from .views import  map_view
from waterbodies_app.views import powaterbodies_list
from .views import metadata_view
from .views import kml_files_list
from .views import tabledesign
from waterbodies_app.views import waterbodies_tank_list
urlpatterns = [
    path('', index, name='index'),
     path('change-password/', change_password, name='change_password'),
    path('admin-login/', admin_login, name='admin_login'),
    path('register/', register_view, name='register'),
      path('user-list/', user_list_view, name='user_list'),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('logout/', views.Logoutview, name='logout'), 
    path('water-bodies/', water_body_list, name='waterbody-list'),
    path('add-water-body/', add_water_body, name='add-water-body'),
    path('api/get-water-body-data/', get_water_body_data, name='get-water-body-data'),
    
    path('delete-water-body-confirmation/<int:waterbody_id>/', delete_water_body_confirmation, name='delete_water_body_confirmation'),
    path('tableau-visualization/', tableau_visualization, name='tableau_visualization'),
    path ('dasboardanalytics/', dashboardanalytics, name='analytics'),
     path('volunteer/', volunteer_form, name='volunteer_form'),
     path('volunteers/', volunteers_list, name='volunteers_list'),
     #path('field-workers/', field_worker_list, name='field_worker_list'),
    path('water_body_details/<int:water_body_id>/', water_body_details, name='water_body_details'),

     path('waterbody-lists/', waterbody_lists, name='waterbody_lists'),

   
   path('api/get-taluk-data/', get_taluk_data, name='get-taluk-data'),
   path('api/get-block-data/', get_block_data, name='get_block_data'),
    #path('field-worker-login/', field_worker_login, name='field_worker_login'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('ponds/', pond_list, name='pond_list'),
    #path('pond/<int:pk>/', pond_detail, name='pond_detail'), 
    #path('get_water_supply_details/<int:pond_id>/', get_water_supply_details, name='get_water_supply_details'),
    path('custom-login/', custom_login_view, name='custom_login'),
    path('upload_kml/', upload_kml, name='upload_kml'),
    path('map/', map_view, name='map_view'),
    path('water-spread-details/', fetch_water_spread_data, name='water_spread_details'),
   #path('register/field-worker/', register_field_worker, name='register_field_worker'),
   path('apii/', views.fetch_api_data, name='fetch_api_data'),
    path('waterbody-reviewer-response/', views.waterbody_reviewer_response, name='waterbody_reviewer_response'),
    path('metadata/', metadata_view, name='metadata_view'),
    path('waterbody-fieldworkers/', views.field_workers, name='fieldworkers'),
    path('powaterbodies/', powaterbodies_list, name='powaterbodies_list'),
     path('kml-files/', kml_files_list, name='kml_files_list'),
     path('govwb/', tabledesign, name='govwb'),
     path('waterbodies-tank/', waterbodies_tank_list, name='waterbodies_tank_list'),
    # Add more URL patterns for your app...
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)