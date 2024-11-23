from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handlelogin, name='handlelogin'),
    path('logout/', views.handlelogout, name='handlelogout'),
    path('bmi/', views.bmi_calculator, name='bmi_calculator'),
    path('delete/', views.delete_users, name='delete_users'),
    path('fitness/', views.fitness_records, name='fitness_records'),
    path('trainer/login/', views.trainer_login, name='trainer_login'),
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('personal-training/', views.personal_training, name='personal_training'),
    path('physical_therapy/', views.physical_therapy, name='physical_therapy'),
    path('group_classes/', views.group_classes, name='group_classes'),
    path('nutrition_council/', views.nutrition_council, name='nutrition_council'),
    path('wellness_program/', views.wellness_program, name='wellness_program'),
    path('our_vision/', views.our_vision, name='our_vision'),
    path('delete_users/', views.delete_users, name='delete_users'),
]
