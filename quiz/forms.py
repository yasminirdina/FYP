import quiz.models
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _

#get all objects (image records) in ImageField table
allFieldImage = quiz.models.ImageField.objects.all().order_by('id')
#get values_list of imageURL in ImageField, ordered by id
imageURLList = list(allFieldImage.values_list('imageURL', flat=True).order_by('id'))
#get values_list of name in ImageField, ordered by id 
imageNameList = list(allFieldImage.values_list('name', flat=True).order_by('id'))
#instantiate ICON_CHOICES
ICON_CHOICES = []

#append empty field ikut length list imageURL tadi
for i in range(len(imageURLList)):
    ICON_CHOICES.append((imageURLList[i], imageNameList[i]))

class AddFieldForm(forms.Form):
    name = forms.CharField(label="Nama bidang kerjaya baharu:", max_length=50, required=True)
    image = forms.ChoiceField(label="Pilih ikon:", choices=ICON_CHOICES, required=True)
    name.widget.attrs.update({'class' : 'name'})
    image.widget.attrs.update({'class' : 'image'})

class ChangeIconForm(forms.Form):
    image = forms.ChoiceField(label="Pilih ikon baharu:", choices=ICON_CHOICES, required=True)
    image.widget.attrs.update({'class' : 'image'})

class AvatarForm(forms.ModelForm):
    """
    def __init__(self, *args, **kwargs):
        super(quiz.models.AvatarGenderImage, self).__init__(*args, **kwargs)
        self.fields['avatarID'].choices = list(quiz.models.Avatar.objects.values_list('id', 'careerName'))
        self.fields['avatarGender'].choices = list(quiz.models.AvatarGender.objects.values_list('id', 'avatarGender'))
        self.fields['imageURL'].choices = list(quiz.models.AvatarGenderImage.objects.values_list('id', 'imageURL'))
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatarID'].widget.attrs.update({'class' : 'avatarid'})
        self.fields['workplace'].widget.attrs.update({'class' : 'workplace'})
        self.fields['avatarGender'].widget.attrs.update({'class' : 'avatargender'})

    class Meta:
        model = quiz.models.AvatarGenderImageFinal
        fields = ['avatarID', 'workplace', 'avatarGender']
        labels = {
            'avatarID': _('Pilih kerjaya avatar anda'),
            'workplace': _('Tempat kerja avatar anda'),
            'avatarGender': _('Pilih jantina avatar anda'),
        }