from django import forms
from django.contrib.auth.models import User 
from .models import BinsStats,BINQRs

class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
    class Meta:
        model=User
        fields = ['username','password']

class Bins(forms.ModelForm):
    qr_data = forms.CharField()
    class Meta:
        model = BinsStats
        fields = ['refreshStats', 'lastRefresh', 'fillUp', 'Area','City']
        widgets = {
            # Specify any custom widgets for fields if needed   
        }
        error_messages = {
            'BinID': {
                'unique': 'This BinID is already in use. Please choose a different one.',
            },
            # Add more specific error messages as needed
        }

class QR(forms.ModelForm):
    Lat = forms.CharField(max_length=40)
    Lon = forms.CharField(max_length=40)
    BinID = forms.CharField(max_length=6)
    class Meta:
        model = BINQRs
        fields = []
        widgets = {
            'data': forms.TextInput(attrs={'type': 'text'}),  # Add this line to ensure it's treated as text
        }