from cProfile import label
from django import forms
from django.forms import ModelForm, ValidationError
import search.models

#create uni form
class createUniversity(ModelForm):
    class Meta:
        model = search.models.University
        fields = ['uni']
        labels = {
            'uni': 'Universiti'
            }

    def clean_uni(self):
        uni = self.cleaned_data.get('uni')
        if not uni:
            raise forms.ValidationError('Bahagian ini diperlukan')

        for instance in search.models.University.objects.all():
            if instance.uni == uni:
                raise forms.ValidationError(uni + ' sudah wujud dalam rekod')
        return uni

# uniCourse bridge
class uniCourseCreate(ModelForm):
    class Meta:
        model = search.models.UniCourseBridge
        fields = ['course']
        labels = {
            'course': 'Kursus'
            }

class jobCourseCreate(ModelForm):
    class Meta:
        model = search.models.JobCourseBridge
        fields = ['course']
        labels = {
            'course': 'Kursus'
            }

#create course form
class createCourse(ModelForm):
    class Meta:
        model = search.models.Course
        fields = '__all__' 

    def clean_course(self):
        course = self.cleaned_data.get('course')
        if not course:
            raise forms.ValidationError('Bahagian ini diperlukan')

        for instance in search.models.Course.objects.all():
            if instance.course == course:
                raise forms.ValidationError(course + ' sudah wujud dalam rekod')
        return course

#create job form
class createJob(ModelForm):
    class Meta:
        model = search.models.Jobs
        fields = '__all__' 
    
    def clean_job(self):
        job = self.cleaned_data.get('job')
        if not job:
            raise forms.ValidationError('Bahagian ini diperlukan')

        for instance in search.models.Jobs.objects.all():
            if instance.job == job:
                raise forms.ValidationError(job + ' sudah wujud dalam rekod')
        return job

    def clean_personality(self):
        personality = self.cleaned_data.get('personality')
        if not personality:
            raise forms.ValidationError('Bahagian ini diperlukan')
        return personality