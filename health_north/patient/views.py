from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, User, Speciality, Review, TypeReview, Appointment, Document, TypeDocument, Place


# Create your views here.

def hello(request):
    return HttpResponse('<h1>Voici ma page de test</h1>')


def morning(request):
    return HttpResponse('<h1>Au revoir</h1>')


def layout(request):
    # template = loader.get_template('patient/layout.html')
    # return HttpResponse(template.render(request=request))
    return render(request, 'patient/layout.html')


@login_required(login_url='Login')
def index(request):
    # user = authenticate()
    # if user is not None:
    #    return render(request, 'patient/index.html')
    # else:
    #    return render(request, 'patient/login.html')
    return render(request, 'patient/index.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            lastname = user.last_name
            # return render(request, 'patient/index.html', {'firstname': firstname})
            return redirect('index')
            # return render(request, 'patient/index.html')
        else:
            messages.error(request, 'Votre nom d\'utilisateur ou votre mot de passe est incorrect, veuillez réessayer.')
            return redirect('login')
    else:
        return render(request, 'patient/login.html')


def my_document(request):
    files = Document.objects.filter(profile__user=request.user) # order_by("-id")
    print(files)
    return render(request, 'patient/documents.html', {'files': files})


def ForgotPassword(request):
    return render(request, 'patient/forgot-password.html')


def ProfilSetting(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('profil-setting')
        else:
            messages.error(request, 'Veuillez corriger l\'erreur ci-dessous. ')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'patient/modifier-profil.html', {'form': form }) #



def TakeAppointment(request):
    return render(request, 'patient/prendre-rdv.html')


def Profil(request):
    info = Profile.objects.filter(user=request.user)
    return render(request, 'patient/profil.html', {'info': info})


def Register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        # confirm_password = request.POST['confirm-password']

        if User.objects.filter(username=username):
            messages.error(request, "Ce nom d'utilisateur est déjà utilisé.")
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, 'Cette adresse email est déjà utilisé sur un compte.')
            return redirect('register')
        if len(username) > 10:
            messages.error(request, "Votre nom d'utilisateur ne doit pas dépasser 10 caractères")
            return redirect('register')
        if len(username) < 5:
            messages.error(request, "Le nom d'utilisateur doit comporter au minimum 5 caractères.")
            return redirect('register')
        if len(password) > 11:

            lowerCase = False
            upperCase = False
            num = False
            special = False

            for char in password:
                if char.isdigit():
                    num = True
                if char.islower():
                    lowerCase = True
                if char.isupper():
                    upperCase = True
                if not char.isalnum():
                    special = True

            if not lowerCase == upperCase == num == special:
                messages.error(request, "Le mot de passe doit comporter au minimum 12 caractères, comprenant des "
                                        "majuscules, des minuscules, des chiffres et des caractères spéciaux.")
                return redirect('register')

        else:
            messages.error(request, "Le mot de passe doit comporter au minimum 12 caractères, comprenant des "
                                    "majuscules, des minuscules, des chiffres et des caractères spéciaux.")
            return redirect('register')

        if not username.isalnum():
            messages.error(request, "Votre nom d'utilisateur doit être alphanumeric")
            return redirect('register')

        my_user = User.objects.create_user(username, email, password)
        my_user.first_name = firstname
        my_user.last_name = lastname
        my_user.save()
        messages.success(request, 'Votre compte a été créé avec succès')
        return redirect('login')

    return render(request, 'patient/register.html')


def appointment(request):
    rdv = Appointment.objects.filter(profile__user=request.user)
    print(rdv)
    return render(request, 'patient/rendez-vous.html', {'rdv': rdv})


def Appointment2(request):
    return render(request, 'patient/rendez-vous2.html')


def Logout(request):
    logout(request)
    messages.success(request, 'Vous vous êtes bien déconnecté.')
    return redirect('login')
