from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    #index
    #path('<student_id>/', views.quizMain, name='index'), #temp
    path('admin/<admin_id>/', views.searchAdmin, name='index-admin'), #admin see main page with edit info
    path('<user_type>/<user_id>/', views.search, name='index-nonadmin'), #only accessible by student, parent & teacher see error page redirect to prev
]