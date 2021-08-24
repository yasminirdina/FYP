from django.urls import path
from . import views

app_name = 'test'
urlpatterns = [
    #admin
    path('admin/<user_id>/', views.testAdmin, name='index-admin'),
    #create,update,delete
    # path('admin/<user_id>/kemaskini/', views.updateTest, name='update-admin'),

    #student 
    path('<user_type>/<user_id>/', views.testMain, name='index-nonadmin'),
    path('<user_type>/<user_id>/mula-ujian', views.testStart, name='test-nonadmin'),

    #student 
    # path('penjaga/<user_id>/', views.testNonadmin, name='index-nonadmin'),
    # path('guru/<user_id>/', views.testNonadmin, name='index-nonadmin'), 
]