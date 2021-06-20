from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    #logout
    path('<user_id>/pengesahan-log-keluar/', views.logoutConfirm, name='logout-confirm'), 
    path('<user_id>/log-keluar/', views.loggingOut, name='logging-out'), 
    #index
    path('admin/<user_id>/', views.dashboardMainAdmin, name='index-admin'),
    path('<user_type>/<user_id>/', views.dashboardMain, name='index-nonadmin'),
    #profile settings
    #path('admin/<user_id>/tetapan-profil/', views.showProfileAdmin, name='profile-settings-admin'),
    path('<user_type>/<user_id>/tetapan-profil/', views.showProfileNonAdmin, name='profile-settings-nonadmin'),
    path('<user_type>/<user_id>/tetapan-profil/tukar-kata-laluan/', views.changePassword, name='change-pass'),
    path('<user_type>/<user_id>/tetapan-profil/kemaskini-profil/', views.editProfile, name='edit-profile'),
    #bookmarks
    path('<user_id>/bookmarks/', views.showBookmarks, name='bookmarks'), #temp
    path('<user_type>/<user_id>/penanda/', views.showBookmarks, name='bookmarks'),
    #reports
    path('<user_id>/reports/', views.showReports, name='reports'), #temp
    path('pelajar/<user_id>/laporan/', views.showReports, name='reports-student'),
    path('penjaga/<user_id>/laporan/', views.showReports, name='reports-parent'),
    path('guru/<user_id>/laporan/', views.showReports, name='reports-teacher'),
    #chat
    path('<user_id>/chat/', views.showChat, name='chat'), #temp
    path('admin/<user_id>/kaunseling/', views.showChat, name='chat-admin'),
    path('pelajar/<user_id>/kaunseling/', views.showChat, name='chat-student'),
    path('penjaga/<user_id>/kaunseling/', views.showChat, name='chat-parent'),
    path('guru/<user_id>/kaunseling/', views.showChat, name='chat-teacher'),
    #suggestions
    #path('<user_id>/suggestions/', views.showSuggestions, name='suggestions'), #temp
    path('admin/<user_id>/cadangan/', views.showSuggestionsAdmin, name='suggestions-admin'),
    path('<user_type>/<user_id>/cadangan/', views.showSuggestionsNonAdmin, name='suggestions-nonadmin'),
]