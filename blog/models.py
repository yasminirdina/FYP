from django.db import models
import dashboard.models
import datetime
from datetime import date

# Create your models here.
class BlogPost(models.Model):
    #default id
    title = models.CharField(max_length=500)
    content = models.TextField()
    datePublished = models.DateField(auto_now_add=True)
    timePublished = models.TimeField(auto_now_add=True)
    lastDateEdited = models.DateField(auto_now=True)
    lastTimeEdited = models.TimeField(auto_now=True)
    noOfShares = models.IntegerField(default=0)
    noOfViews = models.IntegerField(default=0)
    show = models.BooleanField(default=False)

    def __str__(self):
        return "Post ID: " + str(self.id) + ", Title: " + self.title

class BlogPostComment(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    userID = models.ForeignKey('dashboard.User', on_delete=models.SET_NULL, null=True)
    parentCommentID = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    dateTimeComment = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return "Comment ID: " + str(self.id) + ", Post ID: " + str(self.blogPostID.id) + ", Text: " + self.text

class BlogPostBookmark(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    userID = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    dateTimeAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Bookmark ID: " + str(self.id) + ", Post ID: " + str(self.blogPostID.id) + ", User ID: " + self.userID.ID

class BlogPostImage(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    # contentFileURL = models.URLField(max_length=200)
    blogPostImage = models.ImageField(upload_to='images/admin_post_images', blank=True)

    def __str__(self):
        return "Image ID: " + str(self.id) + ", Post ID: " + str(self.blogPostID.id)

class BlogPostVideo(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    # contentFileURL = models.URLField(max_length=200)
    blogPostVideo = models.FileField(upload_to='images/admin_post_videos', blank=True)

    def __str__(self):
        return "Video ID: " + str(self.id) + ", Post ID: " + str(self.blogPostID.id)

class BlogPostViewsUser(models.Model):
    #default id
    userID = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return "Post ID: " + str(self.blogPostID.id) + ", User ID: " + str(self.userID.ID)

class Category(models.Model):
    #default id
    name = models.CharField(max_length=50)

    def __str__(self):
        return "Category ID: " + str(self.id) + ", Name: " + str(self.name)

class BlogPostCategory(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "Post ID: " + str(self.blogPostID.id) + ", Category ID: " + str(self.categoryID.id)