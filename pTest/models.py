from django.db import models
from dashboard.models import Student

class Personality(models.Model):
    personality = models.CharField(max_length=120)

    def __str__(self):
        return self.personality

class Questions(models.Model):
    section = models.ForeignKey(Personality, on_delete=models.CASCADE)
    questionText = models.CharField(max_length=1500)
    # points = models.IntegerField()

    def __str__(self):
        return self.questionText
        # return self.questionText, str(self.section.id)

class StudentTester(models.Model):
    ID = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.ID

class StudentPersonalitySession(models.Model):
    studentID = models.ForeignKey(StudentTester, on_delete=models.PROTECT)
    # personalityID = models.ForeignKey(Personality, on_delete=models.CASCADE)
    rSecScore = models.IntegerField(default=0)
    aSecScore = models.IntegerField(default=0)
    iSecScore = models.IntegerField(default=0)
    sSecScore = models.IntegerField(default=0)
    eSecScore = models.IntegerField(default=0)
    cSecScore = models.IntegerField(default=0)
