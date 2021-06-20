from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    #index (main page) - list all blog posts (latest etc.)
    path('admin/<user_id>/', views.blogMainAdmin, name='index-admin'), #admin url
    path('<user_type>/<user_id>/', views.blogMain, name='index-nonadmin'), #all non admin use same url bc same content function/access
]