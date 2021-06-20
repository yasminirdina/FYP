from django.forms import ModelForm

from .models import pTest

class CreateQuestForm(ModelForm):
    class Meta:
        model = pTest
        fields = ['question', 'option_one', 'option_two', 'option_three']
