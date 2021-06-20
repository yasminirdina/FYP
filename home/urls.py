from django.urls import include, path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.futureCruiseMain, name='index'),
    path('log-masuk/', views.login, name='login'),
    path('log-masuk/admin/', views.loginAdmin, name='login-admin'),
    path('log-masuk/bukan-admin/', views.loginNonAdmin, name='login-nonadmin'),
    path('log-masuk/bukan-admin/tetap-semula-kata-laluan/', views.resetPassword, name='reset-pass'),
    path('daftar-akaun/', views.signUp, name='sign-up'),
]
