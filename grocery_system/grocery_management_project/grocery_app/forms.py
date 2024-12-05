from django import forms
from django.core.exceptions import ValidationError
from .models import data,Product# Replace with your actual model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','password']

        widget={
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = data # Replace with your actual model
#         fields = ['email', 'password', 'confirm_password']
#         widgets = {
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
#             'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'})
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password and confirm_password and password != confirm_password:
#             raise ValidationError("Passwords do not match")

#         return cleaned_data


# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password','password confirmation']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
       

 

#         return cleaned_data
    
class Product_Add_Form(forms.ModelForm):
    class Meta:
        model=Product
        fields=['product_name','image','description','price','category']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),

        }

       

    
