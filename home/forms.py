import dashboard.models
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _

NONADMIN_LOGIN_CHOICES=[
    ('Student','Pelajar'),
    ('Parent', 'Ibu Bapa/Penjaga'),
    ('Teacher', 'Guru'),
]

NONADMIN_SIGNUP_CHOICES=[
    ('NA', '----------------'),
    ('Student','Pelajar'),
    ('Parent', 'Ibu Bapa/Penjaga'),
    ('Teacher', 'Guru'),
]

"""SALUTATION_CHOICES=[
    ('Tun', 'Tun'),
    ('Toh Puan', 'Toh Puan'),
    ('Tan Sri', 'Tan Sri'),
    ('Puan Sri', 'Puan Sri'),
    ('Datuk', 'Datuk'),
    ('Datin', 'Datin'),
    ('Tuan Haji', 'Tuan Haji'),
    ('Puan Hajah', 'Puan Hajah'),
    ('Encik', 'Encik'),
    ('Puan', 'Puan'),
    ('Cik', 'Cik'),
]"""

class LoginFormAdmin(forms.Form):
    username = forms.CharField(label="Sila masukkan nama pengguna admin", max_length=10, required=True)
    password = forms.CharField(label="Sila masukkan kata laluan", widget=forms.PasswordInput, max_length=10, required=True)
    username.widget.attrs.update({'class' : 'username'})
    password.widget.attrs.update({'class' : 'password-field'})

class LoginFormNonAdmin(forms.Form):
    userType = forms.CharField(label="Log masuk sebagai", widget=forms.Select(choices=NONADMIN_LOGIN_CHOICES), required=True)
    email = forms.EmailField(label="Sila masukkan alamat emel", max_length=254, required=True)
    password = forms.CharField(label="Sila masukkan kata laluan", widget=forms.PasswordInput, max_length=10, required=True)
    userType.widget.attrs.update({'class' : 'usertype'})
    email.widget.attrs.update({'class' : 'email'})
    password.widget.attrs.update({'class' : 'password-field'})

class ResetPasswordFormA(forms.Form):
    userType = forms.CharField(label="Log masuk sebagai", widget=forms.Select(choices=NONADMIN_LOGIN_CHOICES), required=True)
    email = forms.EmailField(label="Sila masukkan alamat emel", max_length=254, required=True)
    userType.widget.attrs.update({'class' : 'usertype'})
    email.widget.attrs.update({'class' : 'email'})

class ResetPasswordFormB(forms.Form):
    OTP = forms.CharField(label="", max_length=6, required=True)
    OTP.widget.attrs.update({'class' : 'OTP'})

class ResetPasswordFormC(forms.Form):
    newPass =  forms.CharField(label="Sila masukkan kata laluan baharu", widget=forms.PasswordInput, max_length=10, required=True)
    newPassConfirm =  forms.CharField(label="Sila masukkan kata laluan baharu sekali lagi", widget=forms.PasswordInput, max_length=10, required=True)
    newPass.widget.attrs.update({'class' : 'newPass'})
    newPassConfirm.widget.attrs.update({'class' : 'newPassConfirm'})

class SignUpForm(forms.Form):
    userType = forms.CharField(label="Daftar sebagai", widget=forms.Select(choices=NONADMIN_SIGNUP_CHOICES), required=True)
    email = forms.EmailField(label="Sila masukkan alamat emel", max_length=254, required=True)
    username = forms.CharField(label="Sila masukkan nama panggilan", max_length=10, required=True)
    password = forms.CharField(label="Sila masukkan kata laluan", widget=forms.PasswordInput, max_length=10, required=True)
    userType.widget.attrs.update({'class' : 'usertype'})
    email.widget.attrs.update({'class' : 'email'})
    username.widget.attrs.update({'class' : 'username'})
    password.widget.attrs.update({'class' : 'password-field'})

"""class SignUpFormParentTeacher(forms.Form):
    userType = forms.CharField(label="Daftar sebagai", widget=forms.Select(choices=NONADMIN_CHOICES), required=True)
    email = forms.EmailField(label="Sila masukkan alamat emel", max_length=254, required=True)
    username = forms.CharField(label="Sila masukkan nama panggilan", max_length=10, required=True)
    password = forms.CharField(label="Sila masukkan kata laluan", widget=forms.PasswordInput, max_length=10, required=True) 
    name = forms.CharField(label="Sila masukkan nama penuh anda", max_length=50, required=True)
    salutation = forms.CharField(label="Sila pilih kata hormat anda:", widget=forms.Select(choices=SALUTATION_CHOICES), required=True)
"""