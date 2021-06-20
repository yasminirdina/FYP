from django.db import models

# Create your models here.
class BlogPost(models.Model):
    #default id
    title = models.CharField(max_length=100)
    content = models.TextField()
    datePublished = models.DateField(auto_now_add=False)
    timePublished = models.TimeField(auto_now_add=False)
    lastDateEdited = models.DateField(auto_now=False)
    lastTimeEdited = models.TimeField(auto_now=False)
    noOfShares = models.IntegerField()
    noOfViews = models.IntegerField()

class BlogPostComment(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    userID = models.ForeignKey('dashboard.User', on_delete=models.SET_NULL, null=True)
    parentCommentID = models.ForeignKey('self', on_delete=models.PROTECT)
    text = models.CharField(max_length=200)

class BlogPostBookmark(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    userID = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    dateTimeAdded = models.DateTimeField(auto_now_add=False)

class BlogPostContentFile(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    contentFileURL = models.URLField(max_length=200)

class BlogPostViewsUser(models.Model):
    #default id
    userID = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

class Category(models.Model):
    #default id
    name = models.CharField(max_length=20)

class BlogPostCategory(models.Model):
    #default id
    blogPostID = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)