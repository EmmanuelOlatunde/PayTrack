from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MemberRegistrationForm(UserCreationForm):
    monthly_target = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        initial=3000,
        error_messages={'required': 'Please enter a monthly target.'}
    )

    class Meta:
        model = User
        fields = ('username', 'monthly_target', 'password1', 'password2')
