from django.db import models
from pTest.models import Personality
# blank = required field if false, null = can store kosong if true

class University(models.Model):
    uni = models.CharField(max_length=120, blank=True, null=True)
    rating = models.IntegerField(default=0)
    uniType = models.CharField(max_length=120, blank=True, default="N/A")
    location = models.CharField(max_length=120, blank=True, default="N/A")
    description = models.TextField(blank=True, default="N/A")
    fee = models.CharField(max_length=120, blank=True, default="N/A")
    population = models.CharField(max_length=120, blank=True, default="N/A")
    intStudent = models.BooleanField(default=False)
    contactInfo = models.CharField(max_length=120, blank=True, default="N/A")
    linkPage = models.CharField(max_length=120, blank=True, default="N/A")

    def __str__(self):
        return self.uni

class Course(models.Model):
#     university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.CharField(max_length=120, blank=True, null=True)
    rating = models.IntegerField(default=0)
    studyLevel = models.CharField(max_length=120, blank=True, default="N/A")
    langguage = models.CharField(max_length=120, blank=True, default="N/A")
    avgFee = models.CharField(max_length=120, blank=True, default="N/A")
    avgDuration = models.CharField(max_length=120, blank=True, default="N/A")
    description = models.TextField(blank=True, default="N/A") 
    requirement = models.CharField(max_length=120, blank=True, default="N/A")

    def __str__(self):
        return self.course

class Jobs(models.Model):
    job = models.CharField(max_length=120, blank=True, null=True)
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE)
    description = models.TextField(blank=True, default="N/A") 
    skills = models.CharField(max_length=120, blank=True, default="N/A")
    avgSalary = models.CharField(max_length=120, blank=True, default="N/A")
    avgEmployement = models.CharField(max_length=120, blank=True, default="N/A")

    def __str__(self):
        return self.job

class UniCourseBridge(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    linkUni = models.CharField(max_length=120, blank=True, default="N/A")

    def __str__(self):
        return self.university, self.course

class JobCourseBridge(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.job, self.course