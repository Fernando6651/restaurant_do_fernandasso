from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import ReservationListView  # Ajuste o nome da view de acordo com sua implementação
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.home, name='home'),  # Rota para a página inicial
    path('reservations/', views.reservations_list, name='reservations'),  # Rota para a listagem de reservas
    path('reservations/new/', views.create_reservation, name='create_reservation'),  # Rota para criar nova reserva
    path('login/', auth_views.LoginView.as_view(template_name='restaurant/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),  # Apontando para a nova view personalizada
    path('register/', views.register, name='register'),
    path('menu/', views.menu_view, name='menu'),  # URL para acessar o menu
    path('sobre/', views.sobre_view, name='sobre'),  # Página "Sobre" (se ainda não existir, pode criar uma)
    path('check-availability/', views.check_availability, name='check_availability'),
    path('reservations/', ReservationListView.as_view(), name='reservation-list'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
