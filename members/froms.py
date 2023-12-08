from django import forms
from django.contrib.auth.models import User 
from .models import BinsStats

class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
    class Meta:
        model=User
        fields = ['username','password']

class Bins(forms.ModelForm):
    class Meta:
        model = BinsStats
        fields = ['BinID', 'status', 'refreshStats', 'lastRefresh', 'fillUp', 'Lat', 'Lon', 'Area','City']
        widgets = {
            # Specify any custom widgets for fields if needed   
        }
        error_messages = {
            'BinID': {
                'unique': 'This BinID is already in use. Please choose a different one.',
            },
            # Add more specific error messages as needed
        }