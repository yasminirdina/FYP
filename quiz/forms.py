import quiz.models
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _
from django.forms import BaseFormSet, BaseInlineFormSet
from django.forms.widgets import ClearableFileInput
import quiz.views

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
    """ def __init__(self, *args, **kwargs):
        super(AddQuestionForm, self).__init__(*args, **kwargs)
        for k, field in self.fields.items():
            if 'required' in field.error_messages:
                field.error_messages['required'] = 'Teks soalan tidak boleh dibiarkan kosong.' """

    questionText = forms.CharField(label="Teks soalan:", max_length=1500, widget=forms.Textarea(attrs={"rows":8}), required=True)
    difficulty = forms.ChoiceField(label="Pilih tahap kesukaran:", choices=DIFFICULTY_CHOICES, required=True)
    questionImage = forms.ImageField(label="Pilih gambar sokongan bagi soalan ini:", required=False)
    questionText.widget.attrs.update({'class' : 'questionText'})
    questionImage.widget.attrs.update({'class' : 'questionImage'})
    difficulty.widget.attrs.update({'class' : 'difficulty'})

class AddAnswerForm(forms.Form):
    answerText = forms.CharField(label="Teks jawapan:", max_length=1500, widget=forms.Textarea(attrs={"rows":3}), required=True)
    isCorrect = forms.BooleanField(label="Tandakan kotak ini jika jawapan ini adalah jawapan yang betul:", required=False)
    answerText.widget.attrs.update({'class' : 'answerText'})
    isCorrect.widget.attrs.update({'class' : 'isCorrect'})

class AddHintForm(forms.Form):
    hintText = forms.CharField(label="Teks petunjuk:", max_length=1500, widget=forms.Textarea(attrs={"rows":3}), required=True)
    value = forms.IntegerField(label="Nilai petunjuk:", min_value=3, max_value=5, initial=3, required=True)
    hintImage = forms.ImageField(label="Pilih gambar sokongan bagi petunjuk ini:", required=False)
    hintText.widget.attrs.update({'class' : 'hintText'})
    hintImage.widget.attrs.update({'class' : 'hintImage'})
    value.widget.attrs.update({'class' : 'value'})

class CustomAnswerFormSet(BaseFormSet):
    def clean(self):
        #super().clean()
        if any(self.errors):
            return

        answers = []
        duplicatesText = False
        cntCorrect = 0

        for form in self.forms:
            if form.cleaned_data:
                answerText = form.cleaned_data.get('answerText')
                isCorrect = form.cleaned_data.get('isCorrect')

                if answerText in answers:
                    duplicatesText = True
                answers.append(answerText)

                if isCorrect == True:
                    cntCorrect += 1

                #(3) if adding similar answerText(s)
                if duplicatesText:
                    raise forms.ValidationError(
                        '(3) Semua teks jawapan mestilah unik dan tiada yang sama.',
                        code='duplicate_answers'
                    )
        
        #(4) if tick more than one correct answers
        if cntCorrect > 1:
            raise forms.ValidationError(
                '(4) Anda tidak boleh menanda lebih daripada satu jawapan yang betul.',
                code='multiple_correct'
            )
        #(5) if no correct answer ticked
        elif cntCorrect == 0:
            raise forms.ValidationError(
                '(5) Anda mestilah menanda satu jawapan yang betul.',
                code='no_correct'
            )

class CustomHintFormSet(BaseFormSet):
    def clean(self):
        #super().clean()
        if any(self.errors):
            return

        hints = []
        duplicatesText = False

        for form in self.forms:
            if form.cleaned_data:
                hintText = form.cleaned_data.get('hintText')

                if hintText in hints:
                    duplicatesText = True
                hints.append(hintText)

                #(3) if adding similar answerText(s)
                if duplicatesText:
                    raise forms.ValidationError(
                        '(3) Semua teks petunjuk mestilah unik dan tiada yang sama.',
                        code='duplicate_hints'
                    )
                    
class CustomImageFieldWidget(ClearableFileInput):
    template_name = 'widgets/customclearablefileinput.html'

class EditQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questionText'].widget.attrs.update({'class' : 'questionText'})
        self.fields['questionImage'].widget.attrs.update({'class' : 'questionImage'})
        self.fields['difficulty'].widget.attrs.update({'class' : 'difficulty'})

    class Meta:
        model = quiz.models.GameQuestion
        fields = ['questionText', 'questionImage', 'difficulty']
        labels = {
            'questionText': _('Kemaskini teks soalan'),
            'questionImage': _('Kemaskini gambar sokongan'),
            'difficulty': _('Kemaskini tahap kesukaran soalan'),
        }
        widgets = {
            'questionImage': CustomImageFieldWidget,
        }

class CustomAnswerInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        answers = []
        duplicatesText = False
        cntCorrect = 0
        cntDelete = 0
        cntForm = 0

        for form in self.forms:
            if form.cleaned_data:
                answerText = form.cleaned_data.get('answerText')
                isCorrect = form.cleaned_data.get('isCorrect')
                toDelete = form.cleaned_data.get('DELETE')

                if answerText != None and answerText in answers:
                    duplicatesText = True
                answers.append(answerText)

                if isCorrect == True and toDelete == False:
                    cntCorrect += 1

                if toDelete == True:
                    cntDelete += 1

                #(4) if got same answer text (among existing or among existing+new) 
                if duplicatesText == True:
                    raise forms.ValidationError(
                        '(4) Semua teks jawapan mestilah unik dan tiada yang sama.',
                        code='duplicate_answers'
                    )

                cntForm += 1
        
        #(5) if ticked more than 1 correct answers (existing or existing+new)
        if cntCorrect > 1:
            raise forms.ValidationError(
                '(5) Anda tidak boleh menanda lebih daripada satu jawapan yang betul.',
                code='multiple_correct'
            )
        #(6) if no correct answer ticked (existing or existing+new)
        elif cntCorrect == 0:
            raise forms.ValidationError(
                '(6) Anda mestilah menanda satu jawapan yang betul.',
                code='no_correct'
            )
        
        #(3) if admin tick delete but its already minimum answers needed (leaving empty answers) - paired with error (2) from views.py
        if (cntForm - cntDelete) < self.min_num:
            raise forms.ValidationError(
                '(3) Jumlah minimum pilihan jawapan yang perlu adalah ' + str(self.min_num) + '.',
                code='too_few_forms'
            )

class EditHintForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hintText'].widget.attrs.update({'class' : 'hintText'})
        self.fields['hintImage'].widget.attrs.update({'class' : 'hintImage'})
        self.fields['value'].widget.attrs.update({'class' : 'value'})

    class Meta:
        model = quiz.models.GameHint
        fields = ['hintText', 'hintImage', 'value']
        widgets = {
            'hintImage': CustomImageFieldWidget,
        }

class CustomHintInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        hints = []
        duplicatesText = False

        for form in self.forms:
            if form.cleaned_data:
                hintText = form.cleaned_data.get('hintText')

                if hintText != None and hintText in hints:
                    duplicatesText = True
                hints.append(hintText)

                #(3) if got same hint text (among existing or among existing+new, excluding none/empty) 
                if duplicatesText == True:
                    raise forms.ValidationError(
                        '(3) Semua teks petunjuk mestilah unik dan tiada yang sama.',
                        code='duplicate_hints'
                    )

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

#get all field records ordered by True > False and ascending name order
gameFields = quiz.models.GameField.objects.order_by('-show', 'name')
#get values_list of field name, also ordered by True > False and ascending name order
fieldNameList = list(gameFields.values_list('name', flat=True).order_by('-show', 'name'))
#get all field image records
allFieldImage = quiz.models.ImageField.objects.all()
#instantiate list of field image URL
imageURLList = []

#append image URL into imageURLList following the order of gameFields
for field in gameFields:
    for image in allFieldImage:
        if field.imageURL_id == image.id:
            imageURLList.append(image.imageURL)
            break

#instantiate FIELD_CHOICES
FIELD_CHOICES = []

#append field name and corresponding image URL into FIELD_CHOICES
for i in range(len(fieldNameList)):
    # FIELD_CHOICES.append((fieldNameList[i], imageURLList[i]))
    FIELD_CHOICES.append((fieldNameList[i], fieldNameList[i]))

class ChooseFieldForm(forms.Form):
    name = forms.ChoiceField(label="Pilih bidang kerjaya:", widget=forms.RadioSelect, choices=FIELD_CHOICES, required=True)
    name.widget.attrs.update({'class' : 'name'})

class PlayForm(forms.Form):
    isClicked = forms.CharField(widget=forms.HiddenInput(), max_length=5, required=False)
    answer_choices = forms.ChoiceField(label="Pilih jawapan yang betul:", widget=forms.RadioSelect, choices=[], required=False)
    answer_choices.widget.attrs.update({'class' : 'answer_choices'})

    def __init__(self, answers=None, *args, **kwargs):
        super(PlayForm, self).__init__(*args, **kwargs)
        if answers:
            # for answer in answers:
            self.fields['answer_choices'].choices = answers