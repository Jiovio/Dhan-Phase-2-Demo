# forms.py

from django import forms
from .models import WaterBody, Volunteer
from .models import Worker
from .models import FieldWorker
from django.contrib.auth.forms import AuthenticationForm

class FieldWorkerLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class WaterBodyForm(forms.ModelForm):
    class Meta:
        model = WaterBody
        fields = '__all__'

class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'mobile', 'email', 'volunteering_for', 'taluk', 'block']

    # You can add additional form validation or customization here if needed
class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['username', 'email', 'mobile', 'date_of_birth', 'password']
        
class FieldWorkerForm(forms.ModelForm):
    class Meta:
        model = FieldWorker
        fields = ['username', 'email', 'mobile', 'password']
        widgets = {
            'password': forms.PasswordInput(),  # Render password field as password input
        }
       