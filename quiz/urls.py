from django.urls import include, path

from . import views

app_name = 'quiz'
urlpatterns = [
    #index
    path('admin/<user_id>/', views.quizMainAdmin, name='index-admin'), #admin see main page with table of field - questions - answer - hint
    path('pelajar/<user_id>/', views.quizMain, name='index-student'), #only accessible by student, parent & teacher see error page redirect to prev
    #avatar (STUDENT only)
    path('pelajar/<user_id>/avatar/', views.showAvatar, name='show-avatar'),    
    path('pelajar/<user_id>/avatar/kemaskini/', views.editAvatar, name='edit-avatar'),
    #play (STUDENT only)
    path('pelajar/<user_id>/mula/pilih-bidang/', views.chooseField, name='choose-field'),
    path('pelajar/<user_id>/mula/<field_id>/', views.play, name='quiz-play'),
    path('pelajar/<user_id>/<field_id>/tamat/keputusan/', views.showResult, name='quiz-result'),
    path('pelajar/<user_id>/<field_id>/tamat/kedudukan-pemain/', views.seeRanking, name='quiz-ranking'),
    path('pelajar/<user_id>/<field_id>/tamat/statistik-pemain/', views.seeStatistic, name='quiz-statistic'),
    #questions (ADMIN only)
    path('admin/<user_id>/tetapan-kuiz/bidang/', views.showField, name='show-field'),
    path('admin/<user_id>/tetapan-kuiz/bidang/baharu/', views.addField, name='add-field'),
    path('admin/<user_id>/tetapan-kuiz/bidang/<field_id>/tukar-ikon/', views.changeIcon, name='change-icon'),
    path('admin/<user_id>/tetapan-kuiz/bidang/<field_id>/soalan/', views.showQuestion, name='show-question'),
    path('admin/<user_id>/tetapan-kuiz/bidang/<field_id>/soalan/baharu/', views.addQuestion, name='add-question'),
    path('admin/<user_id>/tetapan-kuiz/bidang/<field_id>/soalan/<question_id>/kemaskini/', views.editQuestion, name='edit-question'),
]