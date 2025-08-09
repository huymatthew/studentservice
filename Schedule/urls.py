from django.urls import path
from . import views

urlpatterns = [
    path('edit/<str:id>/', views.schedule, name='edit'),
    path('export/<str:id>/', views.schedule_export, name='schedule_export'),
    path('add/', views.add_schedule, name='add_schedule'),
    path('create/', views.create_schedule, name='create_schedule'),
    path('delete/<str:id>/<str:subject_id>/', views.delete_schedule, name='delete_schedule'),
]