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
    path('admin/<user_id>/cipta-rekod-baru/universiti', views.createUniData, name='createUniData-admin'),
    path('admin/<user_id>/cipta-rekod-baru/kursus', views.createCourseData, name='createCourseData-admin'),
    path('admin/<user_id>/cipta-rekod-baru/kerjaya', views.createJobData, name='createJobData-admin'),

    path('admin/<user_id>/kemaskini/universiti/<uni_id>', views.updateUniData, name='updateUniData-admin'),
    path('admin/<user_id>/kemaskini/kursus/<course_id>', views.updateCourseData, name='updateCourseData-admin'),
    path('admin/<user_id>/kemaskini/kerjaya/<job_id>', views.updateJobData, name='updateJobData-admin'),
    
    path('admin/<user_id>/padam/universiti/<uni_id>', views.deleteUniData, name='deleteUniData-admin'),
    path('admin/<user_id>/padam/kursus/<course_id>', views.deleteCourseData, name='deleteCourseData-admin'),
    path('admin/<user_id>/padam/kerjaya/<job_id>', views.deleteJobData, name='deleteJobData-admin'),

    #adminPage
    path('admin/<user_id>/kursus/<course_id>', views.courseAdminPage, name='course-AdminPage'),
    path('admin/<user_id>/universiti/<uni_id>', views.uniAdminPage, name='uni-AdminPage'),
    path('admin/<user_id>/kerjaya/<job_id>', views.jobAdminPage, name='job-AdminPage'),
    
    #nonAdmin 
    path('<user_type>/<user_id>/', views.searchMain, name='index-nonadmin'),
    path('<user_type>/<user_id>/cari-semua/', views.searchAll, name='all-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/universiti', views.searchUni, name='uni-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/kursus', views.searchCourse, name='course-nonadmin'),
    path('<user_type>/<user_id>/cari-mengikut/kerjaya', views.searchJobs, name='jobs-nonadmin'),

    #nonAdmin page
    path('<user_type>/<user_id>/kursus/<course_id>', views.coursePage, name='course-page'),
    path('<user_type>/<user_id>/universiti/<uni_id>', views.uniPage, name='uni-page'), 
    path('<user_type>/<user_id>/kerjaya/<job_id>', views.jobPage, name='job-page'),
]