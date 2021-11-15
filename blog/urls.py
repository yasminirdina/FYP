from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    #index (main page) - list all blog posts (latest etc.)
    path('<user_type>/<user_id>/', views.blogMain, name='index'),
    path('<user_type>/<user_id>/senarai-artikel/', views.blogPostList, name='post-list'),
    path('<user_type>/<user_id>/senarai-artikel/artikel/<post_id>', views.viewPost, name='view-post'),
]