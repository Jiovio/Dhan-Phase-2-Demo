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
from .views import fencetype_list, fencetype_update, fencetype_delete
from .views import taluk_list, taluk_update, taluk_delete
from .views import habitation_list, habitation_update, habitation_delete
from .views import taluk_list, taluk_update, taluk_delete
from .views import waterbody_table_view, waterbody_detail_view
from waterbodies_app.views import waterbodies_tank_list
urlpatterns = [
    path('', index, name='index'),
     path('change-password/', change_password, name='change_password'),
    path('admin-login/', admin_login, name='admin_login'),
    path('register/', register_view, name='register'),
      path('user-list/', user_list_view, name='user_list'),
    #path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('logout/', views.Logoutview, name='logout'), 
    #path('water-bodies/', water_body_list, name='waterbody-list'),
    #path('add-water-body/', add_water_body, name='add-water-body'),
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
     path('districts/', views.district_list, name='district_list'),
    path('districts/update/<int:pk>/', views.district_update, name='district_update'),
    path('districts/delete/<int:pk>/', views.district_delete, name='district_delete'),
     
     path('details/', views.details_view, name='details'),
     path('hydrologicaldetails/',views.hydrological_details, name='hydrologicaldetails'),
     path('sourcedetails/',views.source_details, name='sourcedetails'),
      path('watersadetails/',views.watersa_details, name='watersadetails'),
      path('inletdetails/',views.inlet_details, name='inletdetails'),
      path('rwpdetails/',views.rwp_details, name='rwpdetails'),
      path('outletdetails/',views.outlet_details, name='outletdetails'),
       path('fencingdetails/', views.fencing_details, name='fencingdetails'),
       path('functionaldetails/', views.functional_details, name='functionaldetails'),
       path('uniqunessdetails/', views.uniqueness_details, name='uniquenessdetails'),
      path('embankmentdetails/',views.embankment_details, name='embankmentdetails'),
      path('legalissues/',views.legal_issues, name='legalissues'),
      path('encroachment/',views.encroachment, name='encroachment'),
   path('jurisdictions/', views.jurisdiction_list, name='jurisdiction_list'),
    path('jurisdictions/update/', views.jurisdiction_update, name='jurisdiction_update'),
    path('jurisdictions/delete/', views.jurisdiction_delete, name='jurisdiction_delete'),
      path('taluks/', taluk_list, name='taluk_list'),
    path('taluks/update/<int:pk>/', taluk_update, name='taluk_update'),
    path('taluks/delete/<int:pk>/', taluk_delete, name='taluk_delete'),
    path('update-waterbody/<int:pk>/', views.update_waterbody, name='update_waterbody'),  # AJAX-based update
    path('delete-waterbody/<int:pk>/', views.delete_waterbody, name='delete_waterbody'),  # AJAX-based del
    path('roles/', views.roles_table, name='roles_table'),
    path('selectroles/', views.select_roles, name='selectroles'),
     path('fencetypes/', fencetype_list, name='fencetype_list'),
    path('fencetypes/update/<int:pk>/', fencetype_update, name='fencetype_update'),
    path('fencetypes/delete/<int:pk>/', fencetype_delete, name='fencetype_delete'),
    path('tanks/update/<int:tank_id>/', views.update_tank, name='update_tank'),  # View for updating a tank
    path('tanks/delete/<int:tank_id>/', views.delete_tank, name='delete_tank'),  # View for deleting a tank
    path('tanks/', views.waterbodies_tank_list, name='tank_list'), 
     path('habitations/', views.habitation_list, name='habitation_list'),
    path('habitations/update/', views.habitation_update, name='habitation_update'),
    path('habitations/delete/', views.habitation_delete, name='habitation_delete'),
    path('waterbody-details/', water_body_details, name='water_body_details'),
     path('availabilities/', views.availability_list, name='availability_list'),
    path('availabilities/update/', views.availability_update, name='availability_update'),
    path('availabilities/delete/', views.availability_delete, name='availability_delete'),
    path('ayacut-non-cultivation/', views.ayacut_non_cultivation_list, name='ayacut_non_cultivation_list'),
    path('ayacut-non-cultivation/update/', views.ayacut_non_cultivation_update, name='ayacut_non_cultivation_update'),
    path('ayacut-non-cultivation/delete/', views.ayacut_non_cultivation_delete, name='ayacut_non_cultivation_delete'),
    path('boundary/', views.boundary_drop_points_list, name='boundary_drop_points_list'),
    path('boundary/update/', views.boundary_drop_points_update, name='boundary_drop_points_update'),
    path('boundary/delete/', views.boundary_drop_points_delete, name='boundary_drop_points_delete'),
    path('bund-issues/', views.bund_issues_list, name='bund_issues_list'),
    path('bund-issues/update/', views.bund_issues_update, name='bund_issues_update'),
    path('bund-issues/delete/', views.bund_issues_delete, name='bund_issues_delete'),
    path('barrel-types/', views.barrel_type_list, name='barrel_type_list'),
    path('barrel-types/update/', views.barrel_type_update, name='barrel_type_update'),
    path('barrel-types/delete/', views.barrel_type_delete, name='barrel_type_delete'),
    path('bund-functionalities/', views.bund_functionality_list, name='bund_functionality_list'),
    path('bund-functionalities/update/', views.bund_functionality_update, name='bund_functionality_update'),
    path('bund-functionalities/delete/', views.bund_functionality_delete, name='bund_functionality_delete'),
     path('conditions/', views.conditions_list, name='conditions_list'),
    path('conditions/update/', views.conditions_update, name='conditions_update'),
    path('conditions/delete/', views.conditions_delete, name='conditions_delete'),
    path('catchment_types/', views.catchment_type_list, name='catchment_type_list'),
    path('catchment_types/update/', views.catchment_type_update, name='catchment_type_update'),
    path('catchment_types/delete/', views.catchment_type_delete, name='catchment_type_delete'),
     path('water-body/', views.fetch_water_body_data, name='water_body_data'),
     path('pwdtank', views.tank_data_list_view, name='pwdtank_list'),
    path('update/<int:pk>/', views.update_tankdata, name='update_tankdata'),
    path('delete/<int:pk>/', views.delete_tankdata, name='delete_tankdata'),
    
    path('api/waterbody/', views.WaterBodyFieldReviewerReviewDetailListCreateAPIView.as_view(), name='waterbody-list-create'),
    path('api/waterbody/<uuid:pk>/', views.WaterBodyFieldReviewerReviewDetailRetrieveUpdateDestroyAPIView.as_view(), name='waterbody-detail'),
    path('waterbody-table/', waterbody_table_view, name='waterbody-table'),  # Table view
    path('waterbody-detail/<uuid:pk>/', waterbody_detail_view, name='waterbody-detail'),
]
    # Add more URL patterns for your app...

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)