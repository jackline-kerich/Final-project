from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('health_metrics/', views.health_metrics_view, name='health_metrics'),
    path('submit_health_metrics/', views.health_metrics_view, name='submit_health_metrics'),  # Submit form
    path('get_health_metrics/', views.get_health_metrics, name='get_health_metrics'),  # Get data for the chart
    path('mindfulness/', views.mindfulness_view, name='mindfulness'),
    path('save_gratitude/', views.save_gratitude, name='save_gratitude'),
    path('get_affirmation/', views.get_affirmation, name='get_affirmation'),
    path('save_mood/', views.save_mood, name='save_mood'),
    path('community/', views.community_view, name='community'),
    path('evidence-info/', views.evidence_info_view, name='evidence_info'),
    path('evidence-info/<str:category>/', views.evidence_info_view, name='evidence_info_category'),
]