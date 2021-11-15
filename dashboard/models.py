from django.db import models
from django.db.models.fields import NullBooleanField
import django.utils.timezone as timezone
from django.core.validators import MinValueValidator, MaxValueValidator

currentYear = timezone.now().year

# Create your models here.
class User(models.Model):
    ID = models.CharField(max_length=4, primary_key=True)
    adminID = models.CharField(max_length=4, null= True)
    studentID = models.CharField(max_length=4, null=True)
    parentID = models.CharField(max_length=4, null=True)
    teacherID = models.CharField(max_length=4, null=True)
    """
    adminID = models.ForeignKey(Admin, on_delete=models.PROTECT, null=True)
    studentID = models.ForeignKey(Student, on_delete=models.PROTECT, null=True)
    parentID = models.ForeignKey(Parent, on_delete=models.PROTECT, null=True)
    teacherID = models.ForeignKey(Teacher, on_delete=models.PROTECT, null=True)
    """
    username = models.CharField(max_length=10)
    isActive = models.BooleanField()

    def __str__(self):
        return self.ID + " " + str(self.isActive)

class Admin(models.Model):
    ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password = models.CharField(max_length=4096)

    def __str__(self):
        return "Admin " + self.ID.ID

class Parent(models.Model):
    SALUTATION_CHOICES=(
        ('NA', 'NA'),
        ('Tun', 'Tun'),
        ('Toh Puan', 'Toh Puan'),
        ('Tan Sri', 'Tan Sri'),
        ('Puan Sri', 'Puan Sri'),
        ('Datuk', 'Datuk'),
        ('Datin', 'Datin'),
        ('Tuan Haji', 'Tuan Haji'),
        ('Puan Hajah', 'Puan Hajah'),
        ('Encik', 'Encik'),
        ('Puan', 'Puan'),
        ('Cik', 'Cik'),
    ) 

    RELATION_CHOICES=(
        ('NA', 'NA'),
        ('Ibu Kandung', 'Ibu Kandung'),
        ('Bapa Kandung', 'Bapa Kandung'),
        ('Ibu Tiri', 'Ibu Tiri'),
        ('Bapa Tiri', 'Bapa Tiri'),
        ('Ibu Angkat', 'Ibu Angkat'),
        ('Bapa Angkat', 'Bapa Angkat'),
        ('Adik-beradik', 'Adik-beradik'),
        ('Datuk', 'Datuk'),
        ('Nenek', 'Nenek'),
        ('Ibu Saudara', 'Ibu Saudara'),
        ('Bapa Saudara', 'Bapa Saudara'),
        ('Bukan Ahli Keluarga', 'Bukan Ahli Keluarga'),
    )

    ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=4096)
    name = models.CharField(max_length=100, default="NA")
    age = models.CharField(max_length=2, default="NA")
    job = models.CharField(max_length=50, default="NA")
    #relation = models.CharField(max_length=30, default="NA")
    #salutation = models.CharField(max_length=15, default="NA")
    relation = models.CharField(max_length=30, choices=RELATION_CHOICES, default='NA')
    salutation = models.CharField(max_length=15, choices=SALUTATION_CHOICES, default='NA')
    imageURL = models.URLField(max_length=200, default="NA")

    def __str__(self):
        return self.name

class ClassList(models.Model):
    #default id
    name = models.CharField(max_length=25, default="NA")

    def __str__(self):
        return self.name

class Teacher(models.Model):
    SALUTATION_CHOICES=(
        ('NA', 'NA'),
        ('Tun', 'Tun'),
        ('Toh Puan', 'Toh Puan'),
        ('Tan Sri', 'Tan Sri'),
        ('Puan Sri', 'Puan Sri'),
        ('Datuk', 'Datuk'),
        ('Datin', 'Datin'),
        ('Tuan Haji', 'Tuan Haji'),
        ('Puan Hajah', 'Puan Hajah'),
        ('Encik', 'Encik'),
        ('Puan', 'Puan'),
        ('Cik', 'Cik'),
    ) 

    ROLE_CHOICES=(
        ('NA', 'NA'),
        ('Pengetua', 'Pengetua'),
        ('Penolong Kanan', 'Penolong Kanan'),
        ('Guru Bimbingan dan Kaunseling', 'Guru Bimbingan dan Kaunseling'),
        ('Ketua Panitia', 'Ketua Panitia'),
        ('Guru Media', 'Guru Media'),
        ('Guru Data', 'Guru Data'),
        ('Guru Kelas', 'Guru Kelas'),
        ('Guru Mata Pelajaran', 'Guru Mata Pelajaran'),
    )

    #change manual list ni to ikut a table "ClassList"
    """CLASS_CHOICES=(
        ('NA', 'NA'),
        ('5 ARIF', '5 ARIF'),
        ('5 BESTARI', '5 BESTARI'),
        ('5 CENDEKIA', '5 CENDEKIA'),
        ('5 DINAMIK', '5 DINAMIK'),
    )"""

    CLASS_CHOICES = []
    allClassList = ClassList.objects.all()

    for class_name in allClassList:
        CLASS_CHOICES.append((class_name.name, class_name.name))

    ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=4096)
    name = models.CharField(max_length=100, default="NA")
    #salutation = models.CharField(max_length=15, default="NA")
    salutation = models.CharField(max_length=15, choices=SALUTATION_CHOICES, default='NA')
    year = models.IntegerField(default=currentYear, validators=[MinValueValidator(2021), MaxValueValidator(currentYear+1)])
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='NA')
    #role = models.CharField(max_length=50, default="NA")
    homeroomClass = models.CharField(max_length=25, choices=CLASS_CHOICES, default="NA")
    imageURL = models.URLField(max_length=200, default="NA")

    def __str__(self):
        return self.name

class HomeroomTeacherClass(models.Model):
    className = models.CharField(max_length=25, primary_key=True, default="NA")
    teacherID = models.ForeignKey(Teacher, on_delete=models.SET_DEFAULT, default="NA")
    year = models.IntegerField(default=currentYear, validators=[MinValueValidator(2021), MaxValueValidator(currentYear)])

    def __str__(self):
        return self.className

class Student(models.Model):
    ID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parentID = models.ForeignKey(Parent, on_delete=models.SET_DEFAULT, default="NA")
    studentClass = models.ForeignKey(HomeroomTeacherClass, on_delete=models.SET_DEFAULT, default="NA")
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=4096)
    name = models.CharField(max_length=100, default="NA")
    year = models.IntegerField(default=currentYear, validators=[MinValueValidator(2021), MaxValueValidator(currentYear)])
    interest = models.CharField(max_length=50, default="NA")
    imageURL = models.URLField(max_length=200, default="NA")

    def __str__(self):
        return self.name

class SuggestionType(models.Model):
    #default id
    name = models.CharField(max_length=20)

class Suggestion(models.Model):
    #default id
    creatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    typeID = models.ForeignKey(SuggestionType, on_delete=models.SET_NULL, null=True)
    dateIssued = models.DateField(auto_now_add=False)
    timeIssued = models.TimeField(auto_now_add=False)
    title = models.CharField(max_length=30)
    subjectContent = models.CharField(max_length=200)

class Chatroom(models.Model):
    #default id
    nonAdminID = models.ForeignKey(User, on_delete=models.PROTECT)

class Message(models.Model):
    #default id
    creatorID = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by')
    recipientID = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_by')
    parentMessageID = models.OneToOneField('self', on_delete=models.PROTECT, related_name='parent_message_of')
    chatroomID = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    bodyText = models.CharField(max_length=200)
    dateCreated = models.DateField(auto_now_add=False)
    timeCreated = models.TimeField(auto_now_add=False)

class NotificationType(models.Model):
    #default id
    name = models.CharField(max_length=20)

class Notification(models.Model):
    #default id
    senderID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_by')
    recipientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='is_for')
    messageID = models.OneToOneField(Message, on_delete=models.SET_NULL, related_name='message_notif_for', null=True)
    suggestionID = models.OneToOneField(Suggestion, on_delete=models.SET_NULL, related_name='suggestion_notif_for', null=True)
    typeID = models.ForeignKey(NotificationType, on_delete=models.SET_NULL, null=True)
    blogCommentReplyID = models.OneToOneField('blog.BlogPostComment', on_delete=models.SET_NULL, related_name='comment_reply_notif_for', null=True)
    isOpen = models.BooleanField()

class ReportType(models.Model):
    #default id
    name = models.CharField(max_length=30)

class Report(models.Model):
    #default id
    typeID = models.ForeignKey(ReportType, on_delete=models.SET_NULL, null=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    dateCreated = models.DateField(auto_now_add=False)
    title = models.CharField(max_length=50)
    URL = models.URLField(max_length=200)

class InfoDashboardBookmark(models.Model):
    #default id
    #infoDashboardID = models.ForeignKey('repository.id') <-- KIV bc it's Ain's part
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    dateTimeAdded = models.DateTimeField(auto_now_add=False)