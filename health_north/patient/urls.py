"""health_north URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from .froms import CustomAuthForm

#from patient import views # noqa
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html",
                                                    authentication_form=CustomAuthForm,
                                                    redirect_authenticated_user=True), name="login"),
    #path('login/', views._Login, name="login"),
    path('', auth_views.LoginView.as_view(template_name="login.html",
                                                    authentication_form=CustomAuthForm,
                                                    redirect_authenticated_user=True), name="login"),
    path('index/', views.index, name="index"),
    path('document/', views.my_document, name="document"),
    path('forgot-password/', views.ForgotPassword, name="forgot-password"),
    path('profil-setting/', views.ProfilSetting, name="profil-setting"),
    path('email-setting/', views.email_setting, name="email-setting"),
    path('prendre-rdv/', views.TakeAppointment, name="prendre-rdv"),
    path('profil/', views.Profil, name="profil"),
    path('register/', views.register, name="register"),
    path('logout/', views.Logout, name="logout"),
    path('rendez-vous/', views.appointment, name="rendez-vous"),
    path('rendez-vous2/', views.Appointment2, name="rendez-vous2"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)