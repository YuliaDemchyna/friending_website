from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=150)
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ['email', 'password1', 'password2']

#i have to implement forms myself, meaning the logic that dlows f
# i need to accept the data and handle the data that comes from post, handle errors, update the model
# work in new html template, new form functions and new views (handle all of the logic in views)
#
