from django.db import models

class University(models.Model):
    uni = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.uni

class Course(models.Model):
#     university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.CharField(max_length=120)
    studyLevel = models.CharField(max_length=120, default="")
    langguage = models.CharField(max_length=120, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.course

class Jobs(models.Model):
    job = models.CharField(max_length=120, null=True)
    personality = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.job

class UniCourseBridge(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.university, self.course

class JobCourseBridge(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.job, self.course