"""
URL configuration for core app
"""
from django.urls import path
from . import views
from . import views_setup
from . import views_auth
from . import views_subscription

urlpatterns = [
    # Landing page (public)
    path('', views.landing_page, name='landing_page'),
    
    # Role-specific dashboards
    path('dashboard/', views.dashboard, name='dashboard'),  # Company Admin dashboard
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('area-manager/dashboard/', views.area_manager_dashboard_view, name='area_manager_dashboard'),
    path('division-head/dashboard/', views.division_head_dashboard_view, name='division_head_dashboard'),
    path('agent/<str:agent_id>/', views.agent_detail, name='agent_detail'),
    path('train/', views.train_model, name='train_model'),
    path('api/agents/', views.api_agents, name='api_agents'),
    
    # Area Manager routes
    path('area-managers/', views.area_managers_list, name='area_managers_list'),
    path('area-manager/<str:manager_id>/', views.area_manager_dashboard, name='area_manager_dashboard'),
    
    # Division Head routes
    path('division-heads/', views.division_heads_list, name='division_heads_list'),
    path('division-head/<str:head_id>/', views.division_head_dashboard, name='division_head_dashboard'),
    
    # Authentication routes
    path('register/', views_auth.register_company, name='register_company'),
    path('login/', views_auth.login, name='login'),
    path('logout/', views_auth.logout, name='logout'),
    path('api/auth/register/', views_auth.register_company, name='api_register'),
    path('api/auth/login/', views_auth.login, name='api_login'),
    path('api/auth/logout/', views_auth.logout, name='api_logout'),
    path('api/auth/user/', views_auth.get_current_user, name='current_user'),
    path('api/auth/change-password/', views_auth.change_password, name='change_password'),
    
    # User management routes (company admin)
    path('users/', views_auth.user_management_page, name='user_management'),
    path('api/users/', views_auth.list_users, name='list_users'),
    path('api/users/create/', views_auth.create_user, name='create_user'),
    
    # Subscription routes
    path('subscription/', views_subscription.subscription_dashboard, name='subscription_dashboard'),
    path('api/subscription/', views_subscription.get_subscription_info, name='subscription_info'),
    path('api/subscription/update/', views_subscription.update_subscription, name='update_subscription'),
    path('api/subscription/payments/', views_subscription.get_payment_history, name='payment_history'),
    path('api/subscription/record-payment/', views_subscription.record_payment, name='record_payment'),
    path('api/subscription/generate-invoices/', views_subscription.generate_invoices, name='generate_invoices'),
    
    # Setup endpoints (for free tier deployment)
    path('setup-database/', views_setup.setup_database, name='setup_database'),
    path('check-data/', views_setup.check_data, name='check_data'),
]
