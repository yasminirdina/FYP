from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    #admin
    # path('', views.searchAdmin, name='index-admin'),
    path('admin/<user_id>/', views.searchMainAdmin, name='index-admin'),
    path('admin/<user_id>/cari-semua/', views.allAdmin, name='all-admin'),
    path('admin/<user_id>/cari-mengikut/universiti', views.uniAdmin, name='uni-admin'),
    path('admin/<user_id>/cari-mengikut/kursus', views.courseAdmin, name='course-admin'),
    path('admin/<user_id>/cari-mengikut/kerjaya', views.jobsAdmin, name='jobs-admin'),
    #create,update,delete
    path('admin/<user_id>/cipta-rekod-baru/', views.createData, name='createData-admin'),
    path('admin/<user_id>/kemaskini/<str:pk>/', views.updateData, name='updateData-admin'),
    path('admin/<user_id>/padam/<str:pk>/', views.deleteData, name='deleteData-admin'),

    #non admin 
    path('<user_type>/<user_id>/', views.searchMain, name='index-nonadmin'),
    path('<user_type>/<user_id>/cari-semua/', views.searchAll, name='all-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/universiti', views.searchUni, name='uni-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/kursus', views.searchCourse, name='course-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/kerjaya', views.searchJobs, name='jobs-nonadmin'),

    path('<user_type>/<user_id>/kursus/<course_id>', views.coursePage, name='course-page'),
    path('<user_type>/<user_id>/universiti/<uni_id>', views.uniPage, name='uni-page'), 
    path('<user_type>/<user_id>/kerjaya/<job_id>', views.jobPage, name='job-page'),
]