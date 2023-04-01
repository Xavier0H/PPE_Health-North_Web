from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Profile, User, Speciality, Review, TypeReview, Appointment, Document, TypeDocument, Place
from .froms import PasswordChangingForm, EmailChangeForm, EmailChangingForm, RegisterForm, AddProfil


# Create your views here.


# @login_required(login_url='Login')
def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'index.html')


def _Login(request):
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
        return render(request, 'login.html')


@login_required(login_url='Login')
def my_document(request):
    files = Document.objects.filter(profile__user=request.user)  # order_by("-id")
    print(files)
    return render(request, 'documents.html', {'files': files})


def ForgotPassword(request):
    return render(request, 'forgot-password.html')


@login_required(login_url='Login')
def ProfilSetting(request):
    if request.method == 'POST':
        form = PasswordChangingForm(request.user, request.POST)
        # form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('profil-setting')
        else:
            messages.error(request, 'Veuillez corriger l\'erreur ci-dessous. ')
    else:
        form = PasswordChangingForm(request.user)
        # form = PasswordChangeForm(request.user)
    return render(request, 'modifier-profil.html', {'form': form})  #


@login_required(login_url='Login')
def email_setting(request):
    # form = EmailChangeForm(request.user)
    form = EmailChangingForm(request.user)
    if request.method == 'POST':
        # form = EmailChangeForm(request.user, request.POST)
        form = EmailChangingForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'email-setting.html')
        else:
            messages.error(request, 'Veuillez corriger l\'erreur ci-dessous. ')
    else:
        return render(request, 'email-setting.html', {'form': form})


@login_required(login_url='Login')
def TakeAppointment(request):
    return render(request, 'prendre-rdv.html')


@login_required(login_url='Login')
def Profil(request):
    info = Profile.objects.filter(user=request.user)
    return render(request, 'profil.html', {'info': info})


def register(request):
    """Si request = GET si request = POST permet de créer un nouveau compte Client
                          """
    if request.user.is_authenticated:
        return redirect("index")
    context = {'register': RegisterForm(), 'profilAdd': AddProfil()}  #
    if request.method == "POST":
        # request post
        form = RegisterForm(request.POST)
        formRegister = AddProfil(request.POST)
        if form.is_valid() and formRegister.is_valid():
            # on insère la nouvelle user dans la base
            form.save()
            # on récupère les donnee du formulaire
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            # on récupère l'id de cet utilisateur pour ajouter les donnee dans la table client
            user = get_object_or_404(User, username=username, email=email)
            newUser = Profile(user=user,
                              adresse=formRegister.cleaned_data['adresse'],
                              date_of_birth=formRegister.cleaned_data['date_of_birth'])
            newUser.save()
            # on connecte l'utilisateur
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # on redirige vers sont tableau de bord
            return redirect('index')
        else:
            context["register"] = RegisterForm(request.POST)
            context['profilAdd'] = AddProfil(request.POST)
    print(context)
    return render(request, 'register.html', context)


@login_required(login_url='Login')
def appointment(request):
    rdv = Appointment.objects.filter(profile__user=request.user)
    print(rdv)
    return render(request, 'rendez-vous.html', {'rdv': rdv})


@login_required(login_url='Login')
def Appointment2(request):
    return render(request, 'rendez-vous2.html')


def Logout(request):
    logout(request)
    messages.success(request, 'Vous vous êtes bien déconnecté.')
    return redirect('login')
