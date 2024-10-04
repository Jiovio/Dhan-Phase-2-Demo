# forms.py

from django import forms
from .models import WaterBody, Volunteer
from .models import Worker
from .models import FieldWorker
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import KMLFilesz
from .models import Contact
from .models import PoOwaterbody
from waterbodies_app.models import AyacutNonCultivation
from .models import BoundaryDropPoints

class BoundaryDropPointsForm(forms.ModelForm):
    class Meta:
        model = BoundaryDropPoints
        fields = ['name']

class AyacutNonCultivationForm(forms.ModelForm):
    class Meta:
        model = AyacutNonCultivation
        fields = ['name']
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        
class KMLFileForm(forms.ModelForm):
    class Meta:
        model = KMLFilesz
        fields = '__all__'

class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')

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
class WaterbodyFilterForm(forms.Form):
    taluk = forms.CharField(max_length=100, required=False)
    village = forms.CharField(max_length=100, required=False)

# Form for update (reusing the model form)
class PoOwaterbodyForm(forms.ModelForm):
    class Meta:
        model = PoOwaterbody
        fields = '__all__'