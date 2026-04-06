from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'), # auth
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('allTask/', views.allTask, name='allTask'),
    path('addtask/', views.addtask, name='addtask'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('edit/<int:id>/', views.editTask, name='edit'),
    path('dashboard/', views.dashboard, name='dashboard'),
]