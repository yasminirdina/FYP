from django.forms import ModelForm
import search.models

class DataForm(ModelForm):
    class Meta:
        model = search.models.UniCourseBridge
        fields = '__all__'