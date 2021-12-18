import pTest.models
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _
from django.forms import BaseFormSet, BaseInlineFormSet
from django.forms.widgets import ClearableFileInput
import pTest.views

# #get all personality records 
# testPersonality = pTest.models.Personality.objects.all()
# #get values_list of personality
# # The values_list(flat=true) method return a QuerySet of single values: exp: <QuerySet [1, 2]>
# personalityNameList = list(testPersonality.values_list('personality', flat=True))


# #append field name and corresponding image URL into FIELD_CHOICES
# for i in range(len(fieldNameList)):
#     # FIELD_CHOICES.append((fieldNameList[i], imageURLList[i]))
#     FIELD_CHOICES.append((fieldNameList[i], fieldNameList[i]))

# class ChooseFieldForm(forms.Form):
#     name = forms.ChoiceField(label="Pilih bidang kerjaya:", widget=forms.RadioSelect, choices=FIELD_CHOICES, required=True)
#     name.widget.attrs.update({'class' : 'name'})

class TestForm(forms.Form):
    isClicked = forms.CharField(widget=forms.HiddenInput(), max_length=5, required=False)
    answer_choices = forms.ChoiceField(label="Pilih jawapan yang betul:", widget=forms.RadioSelect, choices=[], required=False)
    answer_choices.widget.attrs.update({'class' : 'answer_choices'})

    def __init__(self, answers=None, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        if answers:
            # for answer in answers:
            self.fields['answer_choices'].choices = answers
