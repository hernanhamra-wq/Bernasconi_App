"""
URL configuration for bernasconi_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Auth URLs
    path('auth/', include([
        path('login/', auth_views.LoginView.as_view(
            template_name='registration/login.html'
        ), name='auth_login'),
        # Logout view with confirmation page
        path('logout/', auth_views.LogoutView.as_view(
            template_name='registration/logged_out.html',
            http_method_names=['get', 'post']  # Allow both GET and POST
        ), name='auth_logout'),
    ])),

    # Main application URLs
    path('', include([
        # Root URL - redirects to login
        path('', lambda request: redirect('auth_login'), name='root'),
        # Home page
        path('home/', TemplateView.as_view(
            template_name='home.html'
        ), name='home'),
    ])),
]
