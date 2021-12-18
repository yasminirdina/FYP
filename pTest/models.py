from django.db import models

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

class Student(models.Model):
    ID = models.OneToOneField('dashboard.Student', on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return self.ID

class StudentPersonalitySession(models.Model):
    studentID = models.ForeignKey(Student, on_delete=models.PROTECT)
    personalityID = models.ForeignKey(Personality, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)