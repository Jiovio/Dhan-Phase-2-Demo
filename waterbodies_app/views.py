

# waterbodies_app/views.py
from django.shortcuts import render, get_object_or_404
from .models import WaterBody
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import WaterBody
from django.db.models import Q
from .forms import WaterBodyForm 
from django.http import HttpResponseForbidden
import matplotlib
import matplotlib.pyplot as plt
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
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework import generics
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .serializers import WaterBodySerializer
from rest_framework import permissions
import logging
from .forms import VolunteerForm
from .models import Volunteer
from .forms import FieldWorkerForm
from .models import FieldWorker
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import FieldWorkerLoginForm

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
def index(request):
    waterbodies = WaterBody.objects.all()
    return render(request, 'index.html', {'waterbodies': waterbodies})

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
            return redirect('admin-dashboard')
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



def register_field_worker(request):
    if request.method == 'POST':
        form = FieldWorkerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-dashboard')  # Redirect to admin-dashboard page
    else:
        form = FieldWorkerForm()
    return render(request, 'field_worker_registration.html', {'form': form})

def field_worker_list(request):
    field_workers = FieldWorker.objects.all()
    return render(request, 'field_worker_list.html', {'field_workers': field_workers})
def field_worker_login(request):
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
    
    