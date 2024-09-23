from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Registration Form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Password confirm is not included here

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

# Login Form
class LoginForm(AuthenticationForm):
    pass
# Health Metrics Form
class HealthMetricsForm(forms.Form):
    weight = forms.DecimalField(label="Weight (kg)", required=True, decimal_places=2)
    systolic = forms.IntegerField(label="Systolic Blood Pressure (mm Hg)", required=True)
    diastolic = forms.IntegerField(label="Diastolic Blood Pressure (mm Hg)", required=True)
    sleep_hours = forms.IntegerField(label="Sleep Hours (Daily)", required=True)