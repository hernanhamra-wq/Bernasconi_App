from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('auditoria/', views.auditoria_view, name='auditoria'),
]
