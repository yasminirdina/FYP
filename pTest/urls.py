from django.urls import path
from . import views

app_name = 'pTest'
urlpatterns = [
    #path will further direct ke view file
    #first arg: the remaining path yg dah cut off kat url main 
    #2nd arg: what to display(in this case call out the function in view file)
    #3rd arg: name of the page
     
    path('', views.test, name='test'),
    path('cipta/', views.create, name='create'),
    path('soalan/<pTest_id>/', views.choice, name='choice'),
    path('hasil/<pTest_id>/', views.results, name='result'),
    # path('soalan/', views.questions, name='pTest-question'),
    # path('keputusan/', views.results, name='pTest-results'),
]