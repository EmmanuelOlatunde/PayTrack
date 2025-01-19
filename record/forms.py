from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class MemberRegistrationForm(UserCreationForm):
    monthly_target = forms.DecimalField(max_digits=10, initial=0)

    class Meta:
        model = User
        fields = ('username', 'monthly_target', 'password1', 'password2')
