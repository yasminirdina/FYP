from django.db import models
from django.contrib.auth.models import User

class pTest(models.Model):
   question = models.TextField()
   option_one = models.CharField(max_length=30)
   option_two = models.CharField(max_length=30)
   option_three = models.CharField(max_length=30)
   option_one_count = models.IntegerField(default=0)
   option_two_count = models.IntegerField(default=0)
   option_three_count = models.IntegerField(default=0)

   def total(self):
      return self.option_one_count + self.option_two_count + self.option_two_count

# class Questionnaire(models.Model):
#     questionnaire_text = models.CharField(max_length=200)
#    #  pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.questionnaire_text

# class Question(models.Model):
#     questionnaire = models.ForeignKey(Questionnaire, on_delete = models.CASCADE)
#     question_text = models.CharField(max_length=200)
#    #  pub_date = models.DateTimeField('date published')

#     def __str__(self):
#         return self.question_text

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete = models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     C1 = models.IntegerField(default=0)
#     C2 = models.IntegerField(default=0)
#     N1 = models.IntegerField(default=0)
#     N2 = models.IntegerField(default=0)

# class QuestionnaireInstance (models.Model):

