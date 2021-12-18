from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    #logout
    path('<user_id>/pengesahan-log-keluar/', views.logoutConfirm, name='logout-confirm'), 
    path('<user_id>/log-keluar/', views.loggingOut, name='logging-out'), 
    #index (notification-admin / user-settings-nonadmin)
    path('admin/<user_id>/', views.adminNotif, name='index-admin'),
    path('<user_type>/<user_id>/', views.nonAdminNotif, name='index-nonadmin'),
    #class (admin)/profile (non-admin) settings
    path('admin/<user_id>/tetapan-maklumat-kelas/', views.adminClassSettings, name='class-settings'),
    path('<user_type>/<user_id>/tetapan-profil/', views.showProfileNonAdmin, name='profile-settings'),
    path('<user_type>/<user_id>/tetapan-profil/tukar-kata-laluan/', views.changePassword, name='change-pass'),
    path('<user_type>/<user_id>/tetapan-profil/kemaskini-profil/', views.editProfile, name='edit-profile'), 
    #bookmarks (non-admin)
    path('<user_type>/<user_id>/penanda-isi-kandungan/', views.nonAdminBookmark, name='bookmark'),
    #reports (non-admin)
    path('<user_type>/<user_id>/laporan-visual/', views.nonAdminReport, name='report'), #KIV
    # path('pelajar/<user_id>/laporan/', views.showReports, name='reports-student'), #KIV
    # path('penjaga/<user_id>/laporan/', views.showReports, name='reports-parent'), #KIV
    # path('guru/<user_id>/laporan/', views.showReports, name='reports-teacher'), #KIV
    #chat
    path('admin/<user_id>/ruang-bual-kaunseling/', views.adminChat, name='chat-admin'),
    path('<user_type>/<user_id>/ruang-bual-kaunseling/', views.nonAdminChat, name='chat-nonadmin'), #KIV
    # path('pelajar/<user_id>/ruang-bual-kaunseling/', views.showChat, name='chat-student'), #KIV
    # path('penjaga/<user_id>/ruang-bual-kaunseling/', views.showChat, name='chat-parent'), #KIV
    # path('guru/<user_id>/ruang-bual-kaunseling/', views.showChat, name='chat-teacher'), #KIV
    #suggestions
    path('admin/<user_id>/cadangan/', views.adminSuggestions, name='suggestions-admin'),
    path('<user_type>/<user_id>/cadangan/', views.nonAdminSuggestions, name='suggestions-nonadmin'),
    path('<user_type>/<user_id>/cadangan/baharu/', views.addSuggestion, name='add-suggestion'),
]