from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Profile, User, Speciality, Review, TypeReview, Appointment, Document, TypeDocument, Place, \
    TypePlace, Region, Department, Cities


# Create your views here.

def hello(request):
    return HttpResponse('<h1>Voici ma page de test</h1>')


def morning(request):
    return HttpResponse('<h1>Au revoir</h1>')


def layout(request):
    # template = loader.get_template('patient/layout.html')
    # return HttpResponse(template.render(request=request))
    return render(request, 'patient/layout.html')


def index(request):
    return render(request, 'patient/index.html')


def login(request):
    return render(request, 'patient/login.html')


def Document(request):
    return render(request, 'patient/documents.html')


def ForgotPassword(request):
    return render(request, 'patient/forgot-password.html')


def ProfilSetting(request):
    return render(request, 'patient/modifier-profil.html')


def TakeAppointment(request):
    return render(request, 'patient/prendre-rdv.html')


def Profil(request):
    return render(request, 'patient/profil.html')


def Register(request):
    return render(request, 'patient/register.html')


def Appointment(request):
    return render(request, 'patient/rendez-vous.html')


def Appointment2(request):
    return render(request, 'patient/rendez-vous2.html')
