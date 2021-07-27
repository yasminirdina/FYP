from django.db import models

class University(models.Model):
    uni = models.CharField(max_length=120)

    def __str__(self):
        return self.uni

class Course(models.Model):
#     university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.CharField(max_length=120)

    def __str__(self):
        return self.course

class Bridge(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.university, self.course.course

class Jobs(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    job = models.CharField(max_length=120)

    def __str__(self):
        return self.job
