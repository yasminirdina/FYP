import blog.models
from django import forms
from . import models
from django.utils.translation import ugettext_lazy as _
from tinymce.widgets import TinyMCE

allCategories = blog.models.Category.objects.exclude(name='Tiada').order_by('name')
catNameList = list(allCategories.values_list('name', flat=True))
catIDList = list(allCategories.values_list('id', flat=True))
CATEGORY_CHOICES = []

for i in range(len(catNameList)):
    CATEGORY_CHOICES.append((catIDList[i], catNameList[i]))

CATEGORY_CHOICES.append((1, 'Lain-lain (Kategori baharu)'))

class AddPostForm(forms.Form):
    title = forms.CharField(label="Tajuk artikel:", max_length=500, required=True)
    category = forms.ChoiceField(label="Kategori:", choices=CATEGORY_CHOICES, required=True)
    new_category = forms.CharField(label="Kategori baharu:", max_length=154, required=False)
    description = forms.CharField(label="Rumusan ringkas:", max_length=200, required=True)
    content = forms.CharField(label="Kandungan artikel:", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    isDraft = forms.BooleanField(label="Simpan sebagai draf:", required=False)
    title.widget.attrs.update({'class' : 'title'})
    category.widget.attrs.update({'class' : 'category'})
    new_category.widget.attrs.update({'class' : 'new_category'})
    description.widget.attrs.update({'class' : 'description'})
    content.widget.attrs.update({'class' : 'content'})
    isDraft.widget.attrs.update({'class' : 'isDraft'})

class EditPostForm(forms.Form):
    title = forms.CharField(label="Tajuk artikel:", max_length=500, required=True)
    category = forms.ChoiceField(label="Kategori:", choices=CATEGORY_CHOICES, required=True)
    new_category = forms.CharField(label="Kategori baharu:", max_length=154, required=False)
    description = forms.CharField(label="Rumusan ringkas:", max_length=200, required=True)
    content = forms.CharField(label="Kandungan artikel:", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=True)
    isDraft = forms.BooleanField(label="Simpan sebagai draf:", required=False)
    title.widget.attrs.update({'class' : 'title'})
    category.widget.attrs.update({'class' : 'category'})
    new_category.widget.attrs.update({'class' : 'new_category'})
    description.widget.attrs.update({'class' : 'description'})
    content.widget.attrs.update({'class' : 'content'})
    content.widget.attrs.update({'id' : 'content'})
    isDraft.widget.attrs.update({'class' : 'isDraft'})