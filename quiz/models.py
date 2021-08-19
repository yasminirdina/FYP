import quiz.models
from django.db import models
from django.utils import timezone
from django.urls import reverse
from smart_selects.db_fields import ChainedForeignKey
import dashboard.models
from django.templatetags.static import static

# Create your models here.

class Avatar(models.Model):
    #default id
    careerName = models.CharField(max_length=50)
    #workplace = models.CharField(max_length=100)

    def __str__(self):
        return self.careerName

class AvatarWorkplace(models.Model):
    #default id
    avatarID = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    workplace = models.CharField(max_length=100)

    def __str__(self):
        return self.workplace

class AvatarGender(models.Model):
    #default id
    avatarID = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    avatarGender = models.CharField(max_length=10)

    def __str__(self):
        #return "Avatar ID: " + str(self.avatarID.id) + ", Avatar Career: " + self.avatarID.careerName
        return self.avatarGender

class ImageAvatar(models.Model):
    #default id
    name = models.CharField(max_length=50, default="Tiada Ikon")
    imageURL = models.FilePathField(path="/static/images/quiz_avatar", default="1-default.png")

    @property
    def img_url(self):
        return static("quiz_avatar/{}".format(self.id))

    def __str__(self):
        return self.imageURL

class AvatarGenderImage(models.Model):
    #default id
    avatarID = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    #avatarGender = models.ForeignKey(AvatarGender, on_delete=models.CASCADE)
    avatarGender = ChainedForeignKey(
        AvatarGender,
        chained_field="avatarID",
        chained_model_field="avatarID",
        show_all=False,
        auto_choose=True)
    imageURL = models.URLField(max_length=200)
    name = models.CharField(max_length=50, default="Tiada Ikon")
    #imageURL = models.ForeignKey(ImageAvatar, on_delete=models.SET_DEFAULT, default=1)

    def get_absolute_url(self):
        return reverse('quiz:avatar')

    def __str__(self):
        return self.imageURL

class AvatarGenderImageFinal(models.Model):
    #default id
    avatarID = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    workplace = ChainedForeignKey(
        AvatarWorkplace,
        chained_field="avatarID",
        chained_model_field="avatarID",
        show_all=False,
        auto_choose=True)
    avatarGender = ChainedForeignKey(
        AvatarGender,
        chained_field="avatarID",
        chained_model_field="avatarID",
        show_all=False,
        auto_choose=True)
    imageURL = ChainedForeignKey(
        AvatarGenderImage,
        chained_field="avatarGender",
        chained_model_field="avatarGender",
        show_all=False,
        auto_choose=True)

"""
class AvatarCareer(models.Model):
    #default id
    careerName = models.CharField(max_length=50)
    workplace = models.CharField(max_length=100)
    gender = models.CharField(max_length=6)
    imageURL = models.URLField(max_length=200)

    def __str__(self):
        return "Avatar Career: " + self.careerName
"""

class Player(models.Model):
    #default id
    ID = models.OneToOneField('dashboard.Student', on_delete=models.CASCADE, primary_key=True)
    avatarID = models.ForeignKey(AvatarGenderImageFinal, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return "Player ID: " + self.ID.ID.ID + ", Avatar ID: " + str(self.avatarID.avatarID.id)

class ImageField(models.Model):
    #default id
    #imageURL = models.ImageField(upload_to="quiz_field/")
    name = models.CharField(max_length=50, default="Tiada Ikon")
    imageURL = models.FilePathField(path="/static/images/quiz_field", default="1-default.png")

    @property
    def img_url(self):
        return static("quiz_field/{}".format(self.id))

    def __str__(self):
        return self.imageURL

class GameField(models.Model):
    # default id
    name = models.CharField(max_length=50)
    #imageURL = models.URLField(max_length=200, default="NA")
    imageURL = models.ForeignKey(ImageField, on_delete=models.SET_DEFAULT, default=1)
    show = models.BooleanField(default=False)
    lastEdited = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "Game Field: " + self.name

class FieldPlayerSession(models.Model):
    #default id
    fieldPlayerID = models.ForeignKey(Player, on_delete=models.PROTECT)
    fieldID = models.ForeignKey(GameField, on_delete=models.PROTECT)
    currentPointsEarned = models.IntegerField()
    dateLastPlayed = models.DateTimeField(auto_now=True)
    hintsUsedCount = models.IntegerField(default=0)
    timeTaken = models.DurationField()
    #Check this link for view code: https://laptrinhx.com/how-to-control-the-format-of-a-duration-field-in-django-2259871147/
    totalCorrect = models.IntegerField(default=0)
    countHard = models.IntegerField()
    countHardCorrect = models.IntegerField(default=0)
    countMedium = models.IntegerField()
    countMediumCorrect = models.IntegerField(default=0)
    countEasy = models.IntegerField()
    countEasyCorrect = models.IntegerField(default=0)

    def __str__(self):
        return "Session ID: " + self.id + ", FieldPlayer ID: " + self.fieldPlayerID.playerID.ID.ID + ", Field ID: " + self.fieldID.id

class GameQuestion(models.Model):
    #default id
    fieldID = models.ForeignKey(GameField, on_delete=models.CASCADE)
    questionText = models.CharField(max_length=1500)
    #imageURL = models.URLField(max_length=200, default="NA")
    questionImage = models.ImageField(upload_to='images/admin_questions', blank=True)
    points = models.IntegerField()
    difficulty = models.CharField(max_length=10)
    #careerMention = models.CharField(max_length=100)
    timeLimit = models.CharField(max_length=30)
    lastEdited = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "GameQuestion: " + self.questionText + ", Field ID: " + str(self.fieldID.id)

class GameAnswer(models.Model):
    #default id
    questionID = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    answerText = models.CharField(max_length=1500)
    #imageURL = models.URLField(max_length=200, default="NA")
    isCorrect = models.BooleanField(default=False)

    def __str__(self):
        return "GameAnswer: " + self.answerText + ", QuestionID: " + str(self.questionID.id)

class GameHint(models.Model):
    #default id
    questionID = models.ForeignKey(GameQuestion, on_delete=models.CASCADE)
    #imageURL = models.URLField(max_length=200, default="NA")
    hintImage = models.ImageField(upload_to='images/admin_hints', blank=True)
    hintText = models.CharField(max_length=1500)
    value = models.IntegerField()

    def __str__(self):
        return "GameHint: " + self.hintText + ", QuestionID: " + str(self.questionID.id)