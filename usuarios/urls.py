from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/estilos/', views.style_selector_view, name='style_selector'),
    path('estilos/', views.style_selector_view, name='style_selector'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.inicio, name='inicio'),
]