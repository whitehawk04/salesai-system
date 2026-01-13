"""
URL configuration for core app
"""
from django.urls import path
from . import views
from . import views_setup

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('agent/<str:agent_id>/', views.agent_detail, name='agent_detail'),
    path('train/', views.train_model, name='train_model'),
    path('api/agents/', views.api_agents, name='api_agents'),
    
    # Area Manager routes
    path('area-managers/', views.area_managers_list, name='area_managers_list'),
    path('area-manager/<str:manager_id>/', views.area_manager_dashboard, name='area_manager_dashboard'),
    
    # Division Head routes
    path('division-heads/', views.division_heads_list, name='division_heads_list'),
    path('division-head/<str:head_id>/', views.division_head_dashboard, name='division_head_dashboard'),
    
    # Setup endpoints (for free tier deployment)
    path('setup-database/', views_setup.setup_database, name='setup_database'),
    path('check-data/', views_setup.check_data, name='check_data'),
]
