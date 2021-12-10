from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    #index (main page) - list all blog posts (latest etc.)
    path('<user_type>/<user_id>/', views.blogMain, name='index'),
    path('<user_type>/<user_id>/senarai-artikel/', views.blogPostList, name='post-list'),
    path('<user_type>/<user_id>/senarai-artikel/artikel/<post_id>/', views.viewPost, name='view-post'),
    path('<user_type>/<user_id>/tetapan-blog/baharu/', views.addPost, name='add-post'),
    path('<user_type>/<user_id>/tetapan-blog/artikel/<post_id>/', views.editPost, name='edit-post'),
    # Upload pictures
    path('upload_image/', views.upload_image, name='upload-image'),
]