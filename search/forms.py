from django.forms import ModelForm
from .models import Course, University, Jobs, Bridge

class DataForm(ModelForm):
    class Meta:
        model = Bridge
        fields = '__all__'