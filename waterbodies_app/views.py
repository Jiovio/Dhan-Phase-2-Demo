

# waterbodies_app/views.py
import json
import os
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404
from .models import WaterBody
from waterbodies_app.models import Availability
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Cropings
from .forms import WaterbodyFilterForm, PoOwaterbodyForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import WaterBody
import requests
import zipfile
from django.db.models import Q
from .forms import WaterBodyForm 
from django.http import HttpResponseForbidden
import matplotlib
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .forms import KMLFileForm
from io import BytesIO
import base64
matplotlib.use('Agg')
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from rest_framework.views import APIView
from waterbodies_app.models import WaterbodiesTank
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework import generics
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .serializers import WaterBodySerializer
from rest_framework import permissions
from .models import BarrelType
import logging
from waterbodies_app.models import PoOwaterbody
from .forms import VolunteerForm
from .models import Volunteer
from .forms import FieldWorkerForm
from .models import FieldWorker
from .models import Conditions
from waterbodies_app.forms import AyacutNonCultivationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import FieldWorkerLoginForm
from .forms import CustomLoginForm
from .forms import CustomUserCreationForm
from .models import FenceType
from django.core.files.storage import FileSystemStorage
from .forms import CustomUserCreationForm
from .models import CustomUser
from .models import AyacutNonCultivation
from .models import KMLFilesz
from waterbodies_app.models import District
from django.http import JsonResponse
from xml.etree import ElementTree as ET
from .models import Pond
from .models import Contact
from .forms import ContactForm
from .models import Taluk
from .models import BundFunctionalities
from .models import Habitation

from .models import CatchmentType
from django_filters import FilterSet, CharFilter
from .models import TankData
from .models import BoundaryDropPoints
from .forms import BoundaryDropPointsForm
from .models import BundIssues
from waterbodies_app.models import Jurisdiction
from .models import WaterBodyFieldReviewerReviewDetail
from .serializers import WaterBodyFieldReviewerReviewDetailListSerializer, WaterBodyFieldReviewerReviewDetailSerializer
logger = logging.getLogger(__name__)
def water_body_details(request, water_body_id):
    try:
        water_body = WaterBody.objects.get(id=water_body_id)
        kml_file_path = 'C:\waterbodies_project\static\Kalathi_kanmoi.kml'  # Replace this with the actual path to your KML file
        return render(request, 'water_body_details.html', {'water_body': water_body, 'kml_file_path': kml_file_path})
    except WaterBody.DoesNotExist:
        # Handle the case when the water body is not found
        return render(request, 'water_body_not_found.html')
    except Exception as e:
        # Handle other exceptions
        return render(request, 'error.html', {'error_message': str(e)})
def tableau_visualization(request):
    return render(request, 'map.html')
def tabledesign(request):
    # Get filter values from the request
    taluk_filter = request.GET.get('taluk', '')
    village_filter = request.GET.get('village', '')

    # Fetch all records from the PoOwaterbody model, applying filters
    waterbodies_list = PoOwaterbody.objects.all()

    # Apply filters if they exist
    if taluk_filter:
        waterbodies_list = waterbodies_list.filter(taluk__icontains=taluk_filter)  # Case-insensitive search
    if village_filter:
        waterbodies_list = waterbodies_list.filter(village__icontains=village_filter)  # Case-insensitive search

    # Paginate the records
    paginator = Paginator(waterbodies_list, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    waterbodies = paginator.get_page(page_number)

    # Create a form for each waterbody for the update modal
    forms = {waterbody.id: PoOwaterbodyForm(instance=waterbody) for waterbody in waterbodies}

    # Pass the paginated records and forms to the template
    context = {
        'waterbodies': waterbodies,
        'forms': forms,
        'filter_form': request.GET,  # Include the filter values in the context
    }

    return render(request, 'govwbtable.html', context)

# Update waterbody view (AJAX-based)
def update_waterbody(request, pk):
    waterbody = get_object_or_404(PoOwaterbody, pk=pk)
    if request.method == 'POST':
        form = PoOwaterbodyForm(request.POST, instance=waterbody)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Waterbody updated successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

# Delete waterbody view (AJAX-based)
def delete_waterbody(request, pk):
    waterbody = get_object_or_404(PoOwaterbody, pk=pk)
    if request.method == 'POST':
        waterbody.delete()
        return JsonResponse({'success': True, 'message': 'Waterbody deleted successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})
@login_required(login_url='admin_login')
def dashboardanalytics(request):
    # Get the count of records in the PoOwaterbody model
    waterbodies_count = PoOwaterbody.objects.count()
    
    # Get the count of records in the WaterbodiesTank model
    tanks_count = WaterbodiesTank.objects.count()
    total_tank_data_count = TankData.objects.count() 
    # Fetch all water bodies
    waterbodies = WaterBody.objects.all()

    # Fetch all KML files and convert their URLs to JSON
    fs = FileSystemStorage()
    kml_files = KMLFilesz.objects.all()
    kml_files_json = json.dumps([
        {'kml_file_url': fs.url(kml.kml_file.name)}
        for kml in kml_files
    ])

    # Get a fresh token
    token = get_jwt_token()

    headers = {
        "Authorization": f"JWT {token}"
    }

    # Construct the URL to get the total count of field workers
    field_workers_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/allusers/?limit=1"

    try:
        response = requests.get(field_workers_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        logger.error(f"ConnectionError: Unable to connect to the API - {e}")
        total_field_workers_count = 0  # Set a default value or handle accordingly
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:  # Unauthorized, handle token expiration
            logger.info("Token expired, refreshing token...")
            token = get_jwt_token()
            headers["Authorization"] = f"JWT {token}"
            try:
                response = requests.get(field_workers_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                total_field_workers_count = data.get('count', 0)
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed after refreshing token: {e}")
                total_field_workers_count = 0
        else:
            logger.error(f"HTTPError: {e.response.status_code} - {e.response.text}")
            total_field_workers_count = 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        total_field_workers_count = 0
    else:
        data = response.json()
        total_field_workers_count = data.get('count', 0)

    # Now get the count of water body reviewer responses
    reviewer_response_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterBodyFieldReviewerResponse/?limit=1"

    try:
        response = requests.get(reviewer_response_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        logger.error(f"ConnectionError: Unable to connect to the API - {e}")
        total_reviewer_responses_count = 0  # Set a default value or handle accordingly
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:  # Unauthorized, handle token expiration
            logger.info("Token expired, refreshing token...")
            token = get_jwt_token()
            headers["Authorization"] = f"JWT {token}"
            try:
                response = requests.get(reviewer_response_url, headers=headers)
                response.raise_for_status()
                reviewer_response_data = response.json()
                total_reviewer_responses_count = reviewer_response_data.get('count', 0)
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed after refreshing token: {e}")
                total_reviewer_responses_count = 0
        else:
            logger.error(f"HTTPError: {e.response.status_code} - {e.response.text}")
            total_reviewer_responses_count = 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        total_reviewer_responses_count = 0
    else:
        reviewer_response_data = response.json()
        total_reviewer_responses_count = reviewer_response_data.get('count', 0)

    # Pass the counts, waterbodies, and KML files to the template
    context = {
        'waterbodies_count': waterbodies_count,
        'tanks_count': tanks_count,
        'waterbodies': waterbodies,
        'kml_files_json': kml_files_json,
        'total_field_workers_count': total_field_workers_count,
        'total_reviewer_responses_count': total_reviewer_responses_count,
        'total_tank_data_count': total_tank_data_count,
        
    }

    # Render the dashboard analytical template with the context
    return render(request, 'dashboard_analytical.html', context)

def index(request):
    # Handle POST request for the contact form submission
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('index')  # Redirect to avoid resubmission on page refresh
    else:
        form = ContactForm()

    # Fetch all water bodies
    waterbodies = WaterBody.objects.all()
    waterbodies_count = PoOwaterbody.objects.count()
    
    # Get the count of records in the WaterbodiesTank model
    tanks_count = WaterbodiesTank.objects.count()
    total_tank_data_count = TankData.objects.count() 
    # Fetch all KML files and convert their URLs to JSON
    fs = FileSystemStorage()
    kml_files = KMLFilesz.objects.all()
    kml_files_json = json.dumps([
        {'kml_file_url': fs.url(kml.kml_file.name)}
        for kml in kml_files
    ])

    # Pass water bodies, KML files, and the contact form to the template
    return render(request, 'index.html', {
        'waterbodies': waterbodies,
        'kml_files_json': kml_files_json,
        'waterbodies_count': waterbodies_count,
        'tanks_count': tanks_count,
        'total_tank_data_count': total_tank_data_count,
        'form': form
    })
def admin_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Set session timeout based on "Remember Me" checkbox
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)  # Session expires when the browser is closed

            # Redirect to the admin dashboard or any other page
            return redirect('analytics')
        else:
            error_message = "Invalid username or password."

    return render(request, 'admin_login.html', {'error_message': error_message})
@login_required(login_url='admin_login')
# waterbodies_app/views.py

# ... (existing imports)
def admin_dashboard(request):
    # Retrieve water body data from the database
    water_bodies = WaterBody.objects.all()

    # Prepare data for the initial chart
    initial_chart_data = {
        'data': [{'Tank_Name': body.Tank_Name, 'Cap_MCM': body.Cap_MCM} for body in water_bodies]
    }

    # Prepare data for the taluk distribution chart
    taluk_chart_data = {
        'data': [{'Taluk': body.Taluk} for body in water_bodies]
    }

    # Prepare data for the block distribution chart
    block_chart_data = {
        'data': [{'Block': body.Block} for body in water_bodies]
    }

    return render(
        request,
        'admin_dashboard.html',
        {'waterbodies': water_bodies, 'initial_chart_data': initial_chart_data, 'taluk_chart_data': taluk_chart_data, 'block_chart_data': block_chart_data}
    )



    

def Logoutview(request):
    logout(request)
    return redirect('index')
def water_body_list(request):
    water_bodies = WaterBody.objects.all()

    # Get the search query from the URL parameters
    search_query = request.GET.get('q', '')

    # Apply filtering based on the search query
    if search_query:
        water_bodies = water_bodies.filter(
            Q(Tank_Name__icontains=search_query) |
            Q(Block__icontains=search_query) |
            Q(Taluk__icontains=search_query) |
            Q(District__icontains=search_query) |
            Q(Tank_Name__istartswith=search_query) |  # Match entries starting with the search query
            Q(Block__istartswith=search_query) |  # Match entries starting with the search query
            Q(Taluk__istartswith=search_query) |  # Match entries starting with the search query
            Q(District__istartswith=search_query)  # Match entries starting with the search query
        )

    # Get the selected number of entries per page from the URL parameters
    entries_per_page = request.GET.get('entries_per_page', 10)

    # Pagination
    paginator = Paginator(water_bodies, entries_per_page)
    page = request.GET.get('page')

    try:
        water_bodies = paginator.page(page)
    except PageNotAnInteger:
        water_bodies = paginator.page(1)
    except EmptyPage:
        water_bodies = paginator.page(paginator.num_pages)

    return render(request, 'waterbody_list.html', {'water_bodies': water_bodies, 'search_query': search_query})

def add_water_body(request):
    if request.method == 'POST':
        form = WaterBodyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')
    else:
        form = WaterBodyForm()

    return render(request, 'add_water_body.html', {'form': form})

def get_water_body_data(request):
    # Retrieve water body data from the database
    water_bodies = WaterBody.objects.all()

    # Prepare data for the API response
    data = [{'Tank_Name': body.Tank_Name, 'Cap_MCM': body.Cap_MCM} for body in water_bodies]
    

    return JsonResponse({'data': data})


def delete_water_body_confirmation(request, waterbody_id):
    water_body = get_object_or_404(WaterBody, id=waterbody_id)
    
    if request.method == 'POST':
        # Handle the deletion logic
        water_body.delete()
        return redirect('waterbody-list')  # Redirect to the hospital list

    return render(request, 'delete_confirmation.html', {'water_body': water_body})


def get_taluk_data(request):
    water_bodies = WaterBody.objects.all()
    taluks = set(body.Taluk for body in water_bodies)
    taluk_counts = {taluk: water_bodies.filter(Taluk=taluk).count() for taluk in taluks}

    data = [{'Taluk': taluk, 'Count': count} for taluk, count in taluk_counts.items()]

    return JsonResponse({'data': data})
def get_block_data(request):
    water_bodies = WaterBody.objects.all()
    blocks = set(body.Block for body in water_bodies)
    block_counts = {block: water_bodies.filter(Block=block).count() for block in blocks}

    data = [{'Block': block, 'Count': count} for block, count in block_counts.items()]

    logger.debug('Block data: %s', data)

    return JsonResponse({'data': data})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def volunteer_form(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = "Thank you for volunteering! Your information has been successfully submitted."
            form = VolunteerForm()  # Reset the form for next submission
    else:
        form = VolunteerForm()
        success_message = None  # No success message initially
    return render(request, 'volunteer_form.html', {'form': form, 'success_message': success_message})
def volunteers_list(request):
    volunteers = Volunteer.objects.all()  # Fetch all volunteers from the database
    return render(request, 'volunteer_list.html', {'volunteers': volunteers})



#def register_field_worker(request):
    if request.method == 'POST':
        form = FieldWorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')  # Redirect to admin-dashboard page
    else:
        form = FieldWorkerForm()
    return render(request, 'field_worker_registration.html', {'form': form})

def user_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users})
#def field_worker_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page or dashboard
                return redirect('user_dashboard')  # Update with your desired URL name
    else:
        form = AuthenticationForm(request)
    return render(request, 'field_worker_login.html', {'form': form})
@login_required
def user_dashboard(request):
     # Retrieve water body data from the database
    water_bodies = WaterBody.objects.all()

    # Prepare data for the initial chart
    initial_chart_data = {
        'data': [{'Tank_Name': body.Tank_Name, 'Cap_MCM': body.Cap_MCM} for body in water_bodies]
    }

    # Prepare data for the taluk distribution chart
    taluk_chart_data = {
        'data': [{'Taluk': body.Taluk} for body in water_bodies]
    }

    # Prepare data for the block distribution chart
    block_chart_data = {
        'data': [{'Block': body.Block} for body in water_bodies]
    }

    return render(
        request,
        'user_dashboard.html',
        {'waterbodies': water_bodies, 'initial_chart_data': initial_chart_data, 'taluk_chart_data': taluk_chart_data, 'block_chart_data': block_chart_data}
    )



def waterbody_lists(request):
    water_bodies = WaterBody.objects.all()

    # Get the search query from the URL parameters
    search_query = request.GET.get('q', '')

    # Apply filtering based on the search query
    if search_query:
        water_bodies = water_bodies.filter(
            Q(Tank_Name__icontains=search_query) |
            Q(Block__icontains=search_query) |
            Q(Taluk__icontains=search_query) |
            Q(District__icontains=search_query) |
            Q(Tank_Name__istartswith=search_query) |  # Match entries starting with the search query
            Q(Block__istartswith=search_query) |  # Match entries starting with the search query
            Q(Taluk__istartswith=search_query) |  # Match entries starting with the search query
            Q(District__istartswith=search_query)  # Match entries starting with the search query
        )

    # Get the selected number of entries per page from the URL parameters
    entries_per_page = request.GET.get('entries_per_page', 10)

    # Pagination
    paginator = Paginator(water_bodies, entries_per_page)
    page = request.GET.get('page')

    try:
        water_bodies = paginator.page(page)
    except PageNotAnInteger:
        water_bodies = paginator.page(1)
    except EmptyPage:
        water_bodies = paginator.page(paginator.num_pages)

    return render(request, 'waterbody_lists.html', {'water_bodies': water_bodies, 'search_query': search_query})
    
def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_dashboard')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = CustomLoginForm()
    return render(request, 'field_worker_login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('admin-dashboard')  # Redirect to home or another page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'field_worker_registration.html', {'form': form})

def pond_list(request):
    ponds = Pond.objects.all()
    return render(request, 'pond_list.html', {'ponds': ponds})

def fetch_water_spread_data(request):
    api_url = 'http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterBodyFieldReviewerResponse'  # Replace with your actual API URL
    headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIyMTQxNjExLCJqdGkiOiIyNjc4MTU5ZjA5NTg0YWY0YmI3MGVkM2U4MmUyYmI2MyIsInVzZXJfaWQiOjF9.-zWVM9HmPgbgPTmdrpiPRWOecW8_V6cjweP9yXdc7tM'}  # Add any required headers

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        context = {
            'waterSpreadAreaIssues': data.get('waterSpreadAreaDetails', {}).get('issuesInWaterSpreadArea', '[]'),
            'waterSpreadInvasiveSpecies': data.get('waterSpreadAreaDetails', {}).get('invasiveSpecies', '[]'),
            'percentageOfSpread': data.get('waterSpreadAreaDetails', {}).get('percentageOfSpread', '')
        }
        context['waterSpreadAreaIssues'] = json.loads(context['waterSpreadAreaIssues'])
        context['waterSpreadInvasiveSpecies'] = json.loads(context['waterSpreadInvasiveSpecies'])
        return render(request, 'water_spread_details.html', context)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
def kml_files_list(request):
    fs = FileSystemStorage()
    kml_files = KMLFilesz.objects.all()
    
    # Prepare the data to be displayed
    kml_files_data = []
    for kml in kml_files:
        kml_files_data.append({
            'name': kml.name,
            'file_url': fs.url(kml.kml_file.name)
        })

    return render(request, 'kml_files_list.html', {'kml_files_data': kml_files_data})

def upload_kml(request):
    if request.method == 'POST' and request.FILES.get('kmz_file'):
        kmz_file = request.FILES['kmz_file']
        fs = FileSystemStorage()

        # Save the KMZ file temporarily
        kmz_temp_path = fs.save(kmz_file.name, kmz_file)
        kmz_full_path = fs.path(kmz_temp_path)

        # Extract the KML file from the KMZ
        with zipfile.ZipFile(kmz_full_path, 'r') as kmz:
            kml_files = [f for f in kmz.namelist() if f.endswith('.kml')]
            if kml_files:
                kml_data = kmz.read(kml_files[0])

                # Save the KML file to the media directory
                kml_filename = os.path.splitext(kmz_file.name)[0] + '.kml'
                kml_path = fs.save(os.path.join('kml_files', kml_filename), ContentFile(kml_data))
                
                # Save the KML file information to the database
                KMLFilesz.objects.create(name=kml_filename, kml_file=kml_path)

        # Delete the temporary KMZ file
        fs.delete(kmz_temp_path)

        return redirect('map_view')

    return render(request, 'upload_kml.html')
def map_view(request):
    fs = FileSystemStorage()
    kml_files = KMLFilesz.objects.all()
    kml_files_json = json.dumps([
        {'kml_file_url': fs.url(kml.kml_file.name)}
        for kml in kml_files
    ])
    return render(request, 'map_view.html', {'kml_files_json': kml_files_json})
def metadata_view(request):
    fs = FileSystemStorage()
    kml_files = KMLFilesz.objects.all()
    metadata = []

    for kml in kml_files:
        kml_path = fs.path(kml.kml_file.name)
        
        with open(kml_path, 'r') as f:
            kml_data = f.read()

        # Parse KML to extract metadata
        kml_root = ET.fromstring(kml_data)
        namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

        name = kml_root.find('.//kml:name', namespace).text if kml_root.find('.//kml:name', namespace) is not None else 'Unnamed'
        description = kml_root.find('.//kml:description', namespace).text if kml_root.find('.//kml:description', namespace) is not None else 'No description'
        coordinates = kml_root.find('.//kml:coordinates', namespace).text if kml_root.find('.//kml:coordinates', namespace) is not None else 'No coordinates'

        metadata.append({
            'file_name': kml.name,
            'name': name,
            'description': description,
            'coordinates': coordinates
        })

    return render(request, 'metadata_view.html', {'metadata': metadata})
def fetch_api_data(request):
    # Step 1: Authenticate and obtain JWT token
    auth_url = 'http://waterbody.cloudonweb.in:5000/auth/jwt/create'
    credentials = {
        'username': 'superadmin',  # Replace with your actual username
        'password': '09fghAsd'   # Replace with your actual password
    }
    auth_response = requests.post(auth_url, data=credentials)
    
    if auth_response.status_code == 200:
        token = auth_response.json().get('access_token')
    else:
        token = None

    # Step 2: Use the token to access the protected API
    if token:
        api_url = 'http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterbodytempletanktypes/'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
        else:
            results = []
            print("Failed to fetch data. Response content:", response.content)
    else:
        results = []
        print("Failed to obtain JWT token.")

    # Step 3: Render the data in a template
    return render(request, 'api1.html', {'results': results})
def get_jwt_token():
    auth_url = "http://waterbody.cloudonweb.in:5000/auth/jwt/create"  # Replace with the actual auth URL
    credentials = {
        "username": "superadmin",  # Replace with your username
        "password": "09fghAsd"   # Replace with your password
    }

    response = requests.post(auth_url, data=credentials)
    
    if response.status_code == 200:
        return response.json().get('access')  # Assuming the token is returned under 'access' key
    else:
        raise Exception("Failed to obtain JWT token. Check your credentials.")
def waterbody_reviewer_response(request):
    base_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterBodyFieldReviewerResponse/"
    
    # Get a fresh token
    token = get_jwt_token()

    headers = {
        "Authorization": f"JWT {token}"
    }

    # Get the offset parameter from the URL (default to 340 if not provided)
    offset = int(request.GET.get('offset', 340))
    limit = 10  # Number of items per page

    # Get filter parameters from the request
    survey_number = request.GET.get('surveyNumber', '')
    waterbody_id = request.GET.get('waterbodyId', '')
    waterbody_type = request.GET.get('waterbodyType', '')

    # Construct the URL with the current offset and any filters
    url = f"{base_url}?offset={offset}&limit={limit}"
    
    # Add filter parameters to the URL if they are provided
    if survey_number:
        url += f"&surveyNumber={survey_number}"
    if waterbody_id:
        url += f"&waterbodyId={waterbody_id}"
    if waterbody_type:
        url += f"&waterbodyType={waterbody_type}"

    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Handle token expiration by checking the status code
    if response.status_code == 401:  # Unauthorized
        token = get_jwt_token()
        headers["Authorization"] = f"JWT {token}"
        response = requests.get(url, headers=headers)
    
    data = response.json()

    # Determine next and previous offsets
    next_offset = offset + limit if data.get('next') else None
    previous_offset = offset - limit if offset - limit >= 0 else None

    return render(request, 'waterbody_reviewer_response.html', {
        'data': data.get('results', []),  # Pass the results to the template
        'next_offset': next_offset,
        'previous_offset': previous_offset,
        'current_offset': offset,
        'filter_form': request.GET  # Pass the filter values to the template
    })


    
def powaterbodies_list(request):
    # Fetch all records from the PoOwaterbody model
    waterbodies = PoOwaterbody.objects.all()
    
    # Get the count of the records
    waterbodies_count = waterbodies.count()

    # Pass the records and the count to the template
    context = {
        'waterbodies': waterbodies,
        'waterbodies_count': waterbodies_count
    }

    return render(request, 'powaterbodies_list.html', context)


def waterbodies_tank_list(request):
    # Fetch all tanks
    tank_list = WaterbodiesTank.objects.all()

    # Apply filters if any
    village = request.GET.get('village')
    block = request.GET.get('block')
    panchayat = request.GET.get('panchayat')

    if village:
        tank_list = tank_list.filter(village__icontains=village)
    if block:
        tank_list = tank_list.filter(block__icontains=block)
    if panchayat:
        tank_list = tank_list.filter(panchayat__icontains=panchayat)

    # Apply pagination
    paginator = Paginator(tank_list, 10)  # Show 10 tanks per page
    page_number = request.GET.get('page')

    try:
        tanks = paginator.page(page_number)
    except PageNotAnInteger:
        tanks = paginator.page(1)
    except EmptyPage:
        tanks = paginator.page(paginator.num_pages)

    # Render the template with the paginated and filtered tank list
    return render(request, 'waterbodies_tank_list.html', {'tanks': tanks})


def update_tank(request, tank_id):
    tank = get_object_or_404(WaterbodiesTank, id=tank_id)
    if request.method == 'POST':
        # Update tank fields based on the form submission
        tank.tank_name = request.POST.get('tank_name')
        # Update other fields as necessary
        tank.save()
        return redirect('waterbodies_tank_list')  # Redirect after update
    return render(request, 'update_tank_form.html', {'tank': tank})  # Render form if needed

def delete_tank(request, tank_id):
    tank = get_object_or_404(WaterbodiesTank, id=tank_id)
    if request.method == 'POST':
        tank.delete()
        return redirect('waterbodies_tank_list')  # Redirect after delete
    return render(request, 'confirm_delete.html', {'tank': tank})  # Render confirmation if needed

def field_workers(request):
    base_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/allusers/"
    
    # Get a fresh token
    token = get_jwt_token()

    headers = {
        "Authorization": f"JWT {token}"
    }

    # Get the offset parameter from the URL
    offset = int(request.GET.get('offset', 0))
    limit = 10  # Number of items per page

    # Get the username filter parameter
    username_filter = request.GET.get('username', '')

    # Construct the URL with the current offset and filter
    url = f"{base_url}?offset={offset}&limit={limit}"

    if username_filter:  # Add the username filter to the URL if provided
        url += f"&username={username_filter}"

    response = requests.get(url, headers=headers)
    
    # Handle token expiration by checking the status code
    if response.status_code == 401:  # Unauthorized
        token = get_jwt_token()
        headers["Authorization"] = f"JWT {token}"
        response = requests.get(url, headers=headers)
    
    data = response.json()
    field_workers_count = data.get('count', 0)

    # Determine next and previous offsets
    next_offset = offset + limit if data.get('next') else None
    previous_offset = offset - limit if offset - limit >= 0 else None

    return render(request, 'waterbody_fieldworker.html', {
        'data': data.get('results', []),  # Ensure results are empty if not found
        'next_offset': next_offset,
        'previous_offset': previous_offset,
        'current_offset': offset,
        'field_workers_count': field_workers_count,
        'filter_form': request.GET  # Pass the filter values to the template
    })




def district_list(request):
    districts = District.objects.all()
    return render(request, 'district_list.html', {'districts': districts})

def district_update(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == 'POST':
        district.code = request.POST.get('code')
        district.name = request.POST.get('name')
        district.save()
        return redirect('district_list')
    return render(request, 'district_update.html', {'district': district})

def district_delete(request, pk):
    district = get_object_or_404(District, pk=pk)
    if request.method == 'POST':
        district.delete()
        return redirect('district_list')
    return render(request, 'district_delete.html', {'district': district})


def jurisdiction_list(request):
    jurisdictions = Jurisdiction.objects.all()
    return render(request, 'jurisdiction_list.html', {'jurisdictions': jurisdictions})

def jurisdiction_update(request):
    if request.method == 'POST':
        jurisdiction_id = request.POST.get('id')
        jurisdiction = get_object_or_404(Jurisdiction, pk=jurisdiction_id)
        jurisdiction.code = request.POST.get('code')
        jurisdiction.createdBy = request.POST.get('createdBy')
        jurisdiction.save()
        return redirect('jurisdiction_list')
    return redirect('jurisdiction_list')  # Redirect if not a POST request
def jurisdiction_delete(request):
    if request.method == 'POST':
        jurisdiction_id = request.POST.get('id')
        jurisdiction = get_object_or_404(Jurisdiction, pk=jurisdiction_id)
        jurisdiction.delete()
        return redirect('jurisdiction_list')
    return redirect('jurisdiction_list')  # Handle invalid request by redirecting

def taluk_list(request):
    taluks = Taluk.objects.all()
    return render(request, 'taluk_list.html', {'taluks': taluks})

# View to update a Taluk


def taluk_update(request, pk):
    taluk = get_object_or_404(Taluk, pk=pk)
    if request.method == 'POST':
        taluk.code = request.POST.get('code')
        taluk.name = request.POST.get('name')
        taluk.district_id = request.POST.get('district_id')
        taluk.save()
        return redirect('taluk_list')  # Redirect to the list page after update
    return redirect('taluk_list')  # Handle the case of invalid requests

# View to delete a Taluk
def taluk_delete(request, pk):
    taluk = get_object_or_404(Taluk, pk=pk)
    if request.method == 'POST':
        taluk.delete()
        return redirect('taluk_list')  # Redirect to the list after deletion
    return redirect('taluk_list')  # Handle the case of an invalid request

# View to list all FenceTypes
def fencetype_list(request):
    fencetypes = FenceType.objects.all()
    return render(request, 'fencetype_list.html', {'fencetypes': fencetypes})

# View to update a FenceType
def fencetype_update(request, pk):
    fencetype = get_object_or_404(FenceType, pk=pk)
    if request.method == 'POST':
        fencetype.name = request.POST.get('name')
        fencetype.save()
        return redirect('fencetype_list')
    return render(request, 'fencetype_update.html', {'fencetype': fencetype})

# View to delete a FenceType
def fencetype_delete(request, pk):
    fencetype = get_object_or_404(FenceType, pk=pk)
    if request.method == 'POST':
        fencetype.delete()
        return redirect('fencetype_list')
    return render(request, 'fencetype_delete.html', {'fencetype': fencetype})

def habitation_list(request):
    habitations = Habitation.objects.all()
    paginator = Paginator(habitations, 10)  # Show 10 habitations per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'habitation_list.html', {'page_obj': page_obj})

def habitation_update(request):
    if request.method == 'POST':
        habitation_id = request.POST.get('id')
        habitation = get_object_or_404(Habitation, pk=habitation_id)
        habitation.district_code = request.POST.get('district_code')
        habitation.district = request.POST.get('district')
        habitation.block_code = request.POST.get('block_code')
        habitation.block = request.POST.get('block')
        habitation.village_code = request.POST.get('village_code')
        habitation.village = request.POST.get('village')
        habitation.habitation_code = request.POST.get('habitation_code')
        habitation.habitation = request.POST.get('habitation')
        habitation.save()
        return redirect('habitation_list')

# Delete habitation view
def habitation_delete(request):
    if request.method == 'POST':
        habitation_id = request.POST.get('id')
        habitation = get_object_or_404(Habitation, pk=habitation_id)
        habitation.delete()
        return redirect('habitation_list')
    
def availability_list(request):
    availabilities = Availability.objects.all()
    return render(request, 'availability_list.html', {'availabilities': availabilities})

# Update availability view
def availability_update(request):
    if request.method == 'POST':
        availability_id = request.POST.get('id')
        availability = get_object_or_404(Availability, pk=availability_id)
        availability.name = request.POST.get('name')
        availability.save()
        return redirect('availability_list')

# Delete availability view
def availability_delete(request):
    if request.method == 'POST':
        availability_id = request.POST.get('id')
        availability = get_object_or_404(Availability, pk=availability_id)
        availability.delete()
        return redirect('availability_list')
    
def ayacut_non_cultivation_list(request):
    items = AyacutNonCultivation.objects.all()
    return render(request, 'ayacut_non_cultivation_list.html', {'items': items})

def ayacut_non_cultivation_update(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(AyacutNonCultivation, pk=item_id)
        item.name = request.POST.get('name')
        item.save()
        return redirect('ayacut_non_cultivation_list')

def ayacut_non_cultivation_delete(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = get_object_or_404(AyacutNonCultivation, pk=item_id)
        item.delete()
        return redirect('ayacut_non_cultivation_list')
def boundary_drop_points_list(request):
    boundary_points = BoundaryDropPoints.objects.all()
    return render(request, 'boundarydroppointslist.html', {'boundary_points': boundary_points})

def boundary_drop_points_update(request):
    if request.method == 'POST':
        boundary_point_id = request.POST.get('id')
        boundary_point = get_object_or_404(BoundaryDropPoints, pk=boundary_point_id)
        boundary_point.name = request.POST.get('name')
        boundary_point.save()
        return redirect('boundary_drop_points_list')

def boundary_drop_points_delete(request):
    if request.method == 'POST':
        boundary_point_id = request.POST.get('id')
        boundary_point = get_object_or_404(BoundaryDropPoints, pk=boundary_point_id)
        boundary_point.delete()
        return redirect('boundary_drop_points_list')
    
def bund_issues_list(request):
    bund_issues = BundIssues.objects.all()
    return render(request, 'bund_issues_list.html', {'bund_issues': bund_issues})

# Update bund issue
def bund_issues_update(request):
    if request.method == 'POST':
        bund_issue_id = request.POST.get('id')
        bund_issue = get_object_or_404(BundIssues, pk=bund_issue_id)
        bund_issue.name = request.POST.get('name')
        bund_issue.save()
        return redirect('bund_issues_list')

# Delete bund issue
def bund_issues_delete(request):
    if request.method == 'POST':
        bund_issue_id = request.POST.get('id')
        bund_issue = get_object_or_404(BundIssues, pk=bund_issue_id)
        bund_issue.delete()
        return redirect('bund_issues_list')
def barrel_type_list(request):
    barrel_types = BarrelType.objects.all()
    return render(request, 'barrel_type_list.html', {'barrel_types': barrel_types})

# Update barrel type
def barrel_type_update(request):
    if request.method == 'POST':
        barrel_type_id = request.POST.get('id')
        barrel_type = get_object_or_404(BarrelType, pk=barrel_type_id)
        barrel_type.name = request.POST.get('name')
        barrel_type.save()
        return redirect('barrel_type_list')

# Delete barrel type
def barrel_type_delete(request):
    if request.method == 'POST':
        barrel_type_id = request.POST.get('id')
        barrel_type = get_object_or_404(BarrelType, pk=barrel_type_id)
        barrel_type.delete()
        return redirect('barrel_type_list')
    
def bund_functionality_list(request):
    functionalities = BundFunctionalities.objects.all()
    return render(request, 'bund_functionality_list.html', {'functionalities': functionalities})

# Update bund functionality
def bund_functionality_update(request):
    if request.method == 'POST':
        functionality_id = request.POST.get('id')
        functionality = get_object_or_404(BundFunctionalities, pk=functionality_id)
        functionality.name = request.POST.get('name')
        functionality.save()
        return redirect('bund_functionality_list')

# Delete bund functionality
def bund_functionality_delete(request):
    if request.method == 'POST':
        functionality_id = request.POST.get('id')
        functionality = get_object_or_404(BundFunctionalities, pk=functionality_id)
        functionality.delete()
        return redirect('bund_functionality_list')

def conditions_list(request):
    conditions = Conditions.objects.all()
    return render(request, 'conditions_list.html', {'conditions': conditions})

# Update condition
def conditions_update(request):
    if request.method == 'POST':
        condition_id = request.POST.get('id')
        condition = get_object_or_404(Conditions, pk=condition_id)
        condition.name = request.POST.get('name')
        condition.save()
        return redirect('conditions_list')

# Delete condition
def conditions_delete(request):
    if request.method == 'POST':
        condition_id = request.POST.get('id')
        condition = get_object_or_404(Conditions, pk=condition_id)
        condition.delete()
        return redirect('conditions_list')
def catchment_type_list(request):
    catchment_types = CatchmentType.objects.all()
    return render(request, 'catchment_type_list.html', {'catchment_types': catchment_types})

# Update catchment type
def catchment_type_update(request):
    if request.method == 'POST':
        catchment_type_id = request.POST.get('id')
        catchment_type = get_object_or_404(CatchmentType, pk=catchment_type_id)
        catchment_type.name = request.POST.get('name')
        catchment_type.save()
        return redirect('catchment_type_list')

# Delete catchment type
def catchment_type_delete(request):
    if request.method == 'POST':
        catchment_type_id = request.POST.get('id')
        catchment_type = get_object_or_404(CatchmentType, pk=catchment_type_id)
        catchment_type.delete()
        return redirect('catchment_type_list')
def cropings_list(request):
    cropings = Cropings.objects.all()
    return render(request, 'cropings_list.html', {'cropings': cropings})

# Update croping entry
def cropings_update(request):
    if request.method == 'POST':
        croping_id = request.POST.get('id')
        croping = get_object_or_404(Cropings, pk=croping_id)
        croping.name = request.POST.get('name')
        croping.save()
        return redirect('cropings_list')

# Delete croping entry
def cropings_delete(request):
    if request.method == 'POST':
        croping_id = request.POST.get('id')
        croping = get_object_or_404(Cropings, pk=croping_id)
        croping.delete()
        return redirect('cropings_list')
def details_view(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'details.html', context)

def hydrological_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'hydrologicaldetail.html', context)
def source_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'sourcedetails.html', context)
def watersa_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'watersadetails.html', context)
def embankment_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'embankmentdetails.html', context)

def inlet_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'inletdetails.html', context)

def outlet_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'outletdetails.html', context)
def rwp_details(request):  
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'rwpdetails.html', context)
def fencing_details(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'fencingdetails.html', context)
def functional_details(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'functionalparameter.html', context)
def uniqueness_details(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'uniquenessparameter.html', context)
def legal_issues(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'legalissues.html', context)

def encroachment(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'encroachment.html', context)
def roles_table(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'roles.html', context)
def select_roles(request):
    # You can pass context data to the template if needed
    context = {}
    return render(request, 'selectrole.html', context)
def save_permission(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data['role']
            resource = data['resource']
            permission = data['permission']
            assigned = data['assigned']
            
            # Logic to save the permission in the database (simplified example)
            # Example: update or create a Permission object in the database
            # Permission.objects.update_or_create(role=role, resource=resource, permission=permission, defaults={'assigned': assigned})

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})
def water_body_details(request):
    api_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterBodyFieldReviewerResponse/"
    water_params = {}
    error_message = None

    try:
        # Get the JWT token
        token = get_jwt_token()
        
        # Include the JWT token in the Authorization header
        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Fetch data from the API
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx/5xx)
        
        # Parse the response
        data = response.json()
        water_params = json.loads(data.get('waterParams', '{}'))
        
    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching data from API: {e}"
    except json.JSONDecodeError as e:
        error_message = f"Error parsing JSON: {e}"
    except Exception as e:
        error_message = f"Error obtaining JWT token: {e}"
    
    # Pass the data and error message (if any) to the template
    return render(request, 'waterparams.html', {'water_params': water_params, 'error_message': error_message})

def fetch_water_body_data(request):
    api_url = "http://waterbody.cloudonweb.in:5000/waterBodyAdmin/waterBodyFieldReviewerResponse/14d56954-7aab-44ba-8b7d-2b3b866fac4a/"
    
    try:
        # Make the API request
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Get the main API response data
        data = response.json()

        # Parse the "waterParams" field which is a stringified JSON
        water_params_raw = data.get("waterParams", "{}")
        
        # Safely load the stringified JSON from "waterParams"
        water_params = json.loads(water_params_raw)

    except (requests.RequestException, json.JSONDecodeError) as e:
        # Handle potential errors
        print(f"Error fetching data: {e}")
        return HttpResponse("Error fetching data", status=500)

    # Pass the parsed water_params to the template
    return render(request, 'demofetch.html', {'water_params': water_params})



# The main view that handles listing, filtering, and pagination
def tank_data_list_view(request):
    search_query = request.GET.get('q', '')  # Search query
    filtered_tank_data = TankData.objects.filter(tank_name__icontains=search_query) if search_query else TankData.objects.all()
    
    # Count the total number of tank data entries
    total_tank_data_count = filtered_tank_data.count()

    # Paginate the results (10 entries per page)
    paginator = Paginator(filtered_tank_data, 10)
    page_number = request.GET.get('page')
    paginated_tank_data = paginator.get_page(page_number)

    return render(request, 'tank_data_list.html', {
        'page_obj': paginated_tank_data,
        'search_query': search_query,
        'total_tank_data_count': total_tank_data_count  # Include the count in the context
    })

@csrf_exempt
def update_tankdata(request, pk):
    tank = get_object_or_404(TankData, pk=pk)
    if request.method == 'POST':
        tank.tank_name = request.POST.get('tank_name')
        tank.latitude = request.POST.get('latitude')
        tank.longitude = request.POST.get('longitude')
        tank.save()
        return JsonResponse({'message': 'Tank updated successfully'})

@csrf_exempt
def delete_tankdata(request, pk):
    tank = get_object_or_404(TankData, pk=pk)
    if request.method == 'POST':
        tank.delete()
        return JsonResponse({'message': 'Tank deleted successfully'})
    
class WaterBodyFieldReviewerReviewDetailListCreateAPIView(generics.ListCreateAPIView):
    queryset = WaterBodyFieldReviewerReviewDetail.objects.all()
    serializer_class = WaterBodyFieldReviewerReviewDetailListSerializer

class WaterBodyFieldReviewerReviewDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterBodyFieldReviewerReviewDetail.objects.all()
    serializer_class = WaterBodyFieldReviewerReviewDetailSerializer
    
def waterbody_table_view(request):
    # Fetch all records initially
    waterbodies = WaterBodyFieldReviewerReviewDetail.objects.all()
    
    # Get filter parameters from the request
    block_filter = request.GET.get('block')
    taluk_filter = request.GET.get('taluk')
    waterbody_type_filter = request.GET.get('waterbodyType')
    village_filter = request.GET.get('village')
    waterbody_name_filter = request.GET.get('waterbodyName')
    survey_number_filter = request.GET.get('surveyNumber')
    waterbody_id_filter = request.GET.get('waterbodyId')

    # Apply filters if they are provided
    if block_filter:
        waterbodies = waterbodies.filter(block__icontains=block_filter)
    if taluk_filter:
        waterbodies = waterbodies.filter(taluk__icontains=taluk_filter)
    if waterbody_type_filter:
        waterbodies = waterbodies.filter(waterbodyType=waterbody_type_filter)
    if village_filter:
        waterbodies = waterbodies.filter(village__icontains=village_filter)
    if waterbody_name_filter:
        waterbodies = waterbodies.filter(waterbodyName__icontains=waterbody_name_filter)
    if survey_number_filter:
        waterbodies = waterbodies.filter(surveyNumber__icontains=survey_number_filter)
    if waterbody_id_filter:
        waterbodies = waterbodies.filter(waterbodyId__icontains=waterbody_id_filter)

    # Render the template with the filtered waterbodies
    return render(request, 'testjson.html', {'waterbodies': waterbodies})



def waterbody_detail_view(request, pk):
    # Fetch the water body object by primary key
    waterbody = get_object_or_404(WaterBodyFieldReviewerReviewDetail, pk=pk)

    # Parse the JSON data from the model field
    try:
        waterbody_data = json.loads(waterbody.waterParams)  # Adjust this line based on your model field
    except (ValueError, TypeError):
        waterbody_data = {}

    # Extract relevant data sections
    hydrologic_parameters = waterbody_data.get('hydrologicParamaters', {})
    water_spread_area_details = waterbody_data.get('waterSpreadAreaDetails', {})
    embankment_details = waterbody_data.get('embankmentDetails', {})
    inlet_parameters = waterbody_data.get('inletParameters', {})
    future_activities = waterbody_data.get('futureActivities', {}).get('activitiesUndertaken', "[]")
    
    # Convert future activities string into a list
    future_activities = json.loads(future_activities)

    # Predefined unit rates for activities
    UNIT_RATES = {
        "Earthwork/Desilting/Bund Strengthening": 80,
    "Retaining Wall Construction": 29250,
    "Inlet Construction": 350000,
    "Outlet Construction": 400000,
    "Revetment Construction": 80000,
    "Ghat Construction": 500000,
    "Jungle Clearance": 8,
    "Walking Pavement Construction": 2000,
    "Fencing/Wall Construction": 820,
    "Restoration of Supply Channel": 42,
    "Creation of New Supply Channel": 560,
    "Repair of Sluice": 700000,
    "Surplus Weir": 180000,
    "Tree Plantation": 450,
    "Construction/Repair of Well": 350000,
    "Bund creation": 80,
    }

    # Calculate estimated costs for future activities
    estimated_costs = []
    for activity in future_activities:
        unit_rate = UNIT_RATES.get(activity, 0)  # Use predefined unit rate or 0 if not found
        value = 1  # Assuming a default value of 1; modify as needed for actual values
        estimated_cost = value * unit_rate

        estimated_costs.append({
            'activity': activity,
            'value': value,
            'unit_rate': unit_rate,
            'estimated_cost': estimated_cost,
        })

    # Pass all data sections to the template
    context = {
        'waterbody': waterbody,
        'waterbody_data': waterbody_data,
        'hydrologic_parameters': hydrologic_parameters,
        'water_spread_area_details': water_spread_area_details,
        'embankment_details': embankment_details,
        'inlet_parameters': inlet_parameters,
        'future_activities': future_activities,
        'estimated_costs': estimated_costs,
    }

    return render(request, 'jsondetails.html', context)
