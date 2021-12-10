from django.db import models
from django.db.models.fields import related
import dashboard.models
import datetime
from datetime import date
from tinymce import models as tinymce_models

# Create your models here.
class BlogPost(models.Model):
    #default id
    title = models.CharField(max_length=500)
    content = tinymce_models.HTMLField()
    description = models.CharField(max_length=200, default="Tiada rumusan yang berkenaan bagi artikel ini.")
    datePublished = models.DateField(auto_now_add=True)
    timePublished = models.TimeField(auto_now_add=True)
    lastDateEdited = models.DateField(auto_now=False)
    lastTimeEdited = models.TimeField(auto_now=False)
    noOfShares = models.IntegerField(default=0)
    noOfViews = models.IntegerField(default=0)
    show = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return "Post ID: " + str(self.id) + ", Title: " + self.title

class BlogPostComment(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    userID = models.ForeignKey('dashboard.User', on_delete=models.SET_NULL, null=True)
    parentCommentID = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='parents')
    childCommentID = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='childs')
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

class BlogPostImageTemp(models.Model):
    #default id
    blogPostImage = models.ImageField(upload_to='images/admin_post_images_temp', blank=True)

    def __str__(self):
        return "Image temp ID: " + str(self.id) + ", Image temp URL: " + self.blogPostImage

class BlogPostVideoTemp(models.Model):
    #default id
    blogPostVideo = models.FileField(upload_to='images/admin_post_videos_temp', blank=True)

    def __str__(self):
        return "Video temp ID: " + str(self.id) + ", Video temp URL: " + self.blogPostVideo

class BlogPostViewsUser(models.Model):
    #default id
    userID = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    noOfViews = models.IntegerField(default=0)

    def __str__(self):
        return "Post ID: " + str(self.blogPostID.id) + ", User ID: " + self.userID.ID

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