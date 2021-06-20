from django import forms, http
from django.forms.widgets import Select
from django.http import request
from . import models
import dashboard.models
from django.utils.translation import ugettext_lazy as _

class ChangePasswordForm(forms.Form):
    currentPass = forms.CharField(label="Sila masukkan kata laluan semasa", widget=forms.PasswordInput, max_length=10, required=True)
    newPass =  forms.CharField(label="Sila masukkan kata laluan baharu", widget=forms.PasswordInput, max_length=10, required=True)
    newPassConfirm =  forms.CharField(label="Sila masukkan kata laluan baharu sekali lagi", widget=forms.PasswordInput, max_length=10, required=True)

    currentPass.widget.attrs.update({'class' : 'currentpass'})
    newPass.widget.attrs.update({'class' : 'newpass'})
    newPassConfirm.widget.attrs.update({'class' : 'newpassconfirm'})
"""
class EditProfileStudentForm(forms.Form):
    name = forms.CharField(label="Sila masukkan nama penuh anda (Format: Ali Bin Abu)", max_length=50),
    year = forms.IntegerField(label="Sila masukkan tahun semasa mengikut kalendar (Format: 2021)"),
    className = forms.CharField(label="Sila pilih kelas anda", widget=forms.Select(choices=CLASS_CHOICES)),
    #homeroomTeacher = forms.CharField(label="Guru kelas anda", max_length=50), #nak auto isi ikut className
    interest = forms.CharField(label="Sila masukkan bidang kerjaya yang anda minati sekarang", max_length=20),
    parentName = forms.CharField(label="Sila masukkan nama penuh ibu bapa/penjaga anda", max_length=50)
"""
"""
class_list = list(dashboard.models.HomeroomTeacherClass.objects.values_list('className', flat=True).order_by('className'))
CLASS_CHOICES = []

for i in range(len(class_list)):
    CLASS_CHOICES.append((class_list[i], class_list[i]))

parentIDname_list = list(dashboard.models.Parent.objects.values_list('ID', 'name').order_by('name'))
PARENT_CHOICES = []

for j in range(len(parentIDname_list)):
    PARENT_CHOICES.append((dashboard.models.Parent.objects.get(ID=parentIDname_list[i][0]), parentIDname_list[i][1]))
"""

class EditProfileStudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'name'})
        self.fields['year'].widget.attrs.update({'class' : 'year'})
        self.fields['studentClass'].widget.attrs.update({'class' : 'studentclass'})
        self.fields['interest'].widget.attrs.update({'class' : 'interest'})
        self.fields['parentID'].widget.attrs.update({'class' : 'parentid'})

    class Meta:
        model = models.Student
        #StudentRecord = models.Student.objects.get(ID=request.user_id)
        #ParentOfStudentRecord = models.Parent.objects.get(ID=StudentRecord.parentID)
        fields = ['name', 'year', 'studentClass', 'interest', 'parentID']
        #studentClass = forms.CharField(widget=forms.Select(choices=CLASS_CHOICES))
        #parentID = forms.ChoiceField(choices=PARENT_CHOICES)
        labels = {
            'name': _('Sila masukkan nama penuh anda (Format: Ali Bin Abu)'),
            'year': _('Sila kemaskini tahun semasa'),
            'studentClass': _('Sila pilih kelas anda'),
            'interest': _('Sila masukkan bidang kerjaya yang anda minati sekarang'),
            'parentID': _('Sila pilih nama penuh ibu bapa/penjaga anda'),
        }

class EditProfileParentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'name'})
        self.fields['salutation'].widget.attrs.update({'class' : 'salutation'})
        self.fields['age'].widget.attrs.update({'class' : 'age'})
        self.fields['job'].widget.attrs.update({'class' : 'job'})
        self.fields['relation'].widget.attrs.update({'class' : 'relation'})

    class Meta:
        model = models.Parent
        fields = ['name', 'salutation', 'age', 'job', 'relation']
        labels = {
            'name': _('Sila masukkan nama penuh anda (Format: Ali Bin Abu)'),
            'salutation': _('Sila pilih gelaran anda'),
            'age': _('Sila masukkan umur anda (Format: 48)'),
            'job': _('Sila masukkan pekerjaan semasa anda (Format: Pegawai Perubatan)'),
            'relation': _('Sila pilih hubungan dengan pelajar'),
        }

class EditProfileTeacherForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'name'})
        self.fields['salutation'].widget.attrs.update({'class' : 'salutation'})
        self.fields['role'].widget.attrs.update({'class' : 'role'})
        self.fields['year'].widget.attrs.update({'class' : 'year'})
        self.fields['homeroomClass'].widget.attrs.update({'class' : 'homeroomclass'})

    class Meta:
        model = models.Teacher
        fields = ['name', 'salutation', 'role', 'year', 'homeroomClass']
        labels = {
            'name': _('Sila masukkan nama penuh anda (Format: Ali Bin Abu)'),
            'salutation': _('Sila pilih gelaran anda'),
            'role': _('Sila pilih jawatan anda di sekolah'),
            'year': _('Sila kemaskini tahun semasa yang selaras dengan jawatan di atas'),
            'homeroomClass': _('(Untuk Guru Kelas sahaja) Sila pilih kelas jagaan anda'),
        }

"""
class AvatarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(quiz.models.AvatarGenderImage, self).__init__(*args, **kwargs)
        self.fields['avatarID'].choices = list(quiz.models.Avatar.objects.values_list('id', 'careerName'))
        self.fields['avatarGender'].choices = list(quiz.models.AvatarGender.objects.values_list('id', 'avatarGender'))
        self.fields['imageURL'].choices = list(quiz.models.AvatarGenderImage.objects.values_list('id', 'imageURL'))
    class Meta:
        model = quiz.models.AvatarGenderImageFinal
        fields = ['avatarID', 'workplace', 'avatarGender', 'imageURL']
        labels = {
            'avatarID': _('Pilih kerjaya avatar anda'),
            'workplace': _('Tempat kerja avatar anda'),
            'avatarGender': _('Pilih jantina avatar anda'),
            'imageURL': _('Ikon avatar anda'),
        }
"""