from django.urls import path
from . import views

app_name = 'vitrine'

urlpatterns = [
    path('', views.index, name='index'),
    path('materiel/<int:pk>/', views.materiel_detail, name='detail'),
    path('admin-auth/', views.admin_login_force, name='admin_login_force'),
    
    # Nouvelles routes
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/events/', views.manage_events, name='manage_events'),
    path('admin-dashboard/users/', views.manage_users, name='manage_users'),
    path('user-dashboard/my-events/', views.my_events, name='my_events'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('panier/', views.panier_detail, name='panier_detail'),
    path('panier/add/<int:materiel_id>/', views.panier_add, name='panier_add'),
    path('panier/remove/<int:materiel_id>/', views.panier_remove, name='panier_remove'),
    path('admin-login/', views.AdminLoginView.as_view(), name='admin_login'),
]
