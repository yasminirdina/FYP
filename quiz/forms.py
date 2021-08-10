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

DIFFICULTY_CHOICES = [
    ('Mudah', 'Mudah'),
    ('Sederhana', 'Sederhana'),
    ('Sukar', 'Sukar')
]

class AddFieldForm(forms.Form):
    name = forms.CharField(label="Nama bidang kerjaya baharu:", max_length=50, required=True)
    image = forms.ChoiceField(label="Pilih ikon:", choices=ICON_CHOICES, required=True)
    name.widget.attrs.update({'class' : 'name'})
    image.widget.attrs.update({'class' : 'image'})

class AddQuestionForm(forms.Form):
    questionText = forms.CharField(label="Teks soalan:", max_length=500, widget=forms.Textarea(attrs={"rows":8}), required=True)
    difficulty = forms.ChoiceField(label="Pilih tahap kesukaran:", choices=DIFFICULTY_CHOICES, required=True)
    questionImage = forms.ImageField(label="Pilih gambar sokongan bagi soalan ini:", required=False)
    questionText.widget.attrs.update({'class' : 'questionText'})
    questionImage.widget.attrs.update({'class' : 'questionImage'})
    difficulty.widget.attrs.update({'class' : 'difficulty'})

class AddAnswerForm(forms.Form):
    answerText = forms.CharField(label="Teks jawapan:", max_length=500, widget=forms.Textarea(attrs={"rows":3}), required=True)
    isCorrect = forms.BooleanField(label="Tandakan kotak ini jika jawapan ini adalah jawapan yang betul:", required=False)
    answerText.widget.attrs.update({'class' : 'answerText'})
    isCorrect.widget.attrs.update({'class' : 'isCorrect'})

class AddHintForm(forms.Form):
    hintText = forms.CharField(label="Teks petunjuk:", max_length=500, widget=forms.Textarea(attrs={"rows":3}), required=True)
    value = forms.IntegerField(label="Nilai petunjuk:", min_value=3, max_value=7, initial=3, required=True)
    hintImage = forms.ImageField(label="Pilih gambar sokongan bagi petunjuk ini:", required=False)
    hintText.widget.attrs.update({'class' : 'hintText'})
    hintImage.widget.attrs.update({'class' : 'hintImage'})
    value.widget.attrs.update({'class' : 'value'})

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