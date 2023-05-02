from django import forms
from django.contrib.auth.forms import SetPasswordForm
# from pkg_resources import _
from django.utils.translation import gettext as _
from .models import User, Appointment, SpecialityName, Speciality, Place, Review, Profile
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form, TextInput, DateInput, EmailInput, CharField, EmailField, PasswordInput, DateField
# from .views import take_appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'


class Appointment1Form(forms.ModelForm):
    speciality_name = forms.ModelChoiceField(
        queryset=SpecialityName.objects.all(),
        label='Spécialité',
        widget=forms.Select(
            attrs={'id': 'id_speciality_name'}),
    )
    specialist_name = forms.ModelChoiceField(
        queryset=Speciality.objects.none(),
        label='Spécialiste',
        widget=forms.Select(
            attrs={'id': 'id_specialist_name'}),
    )
    review = forms.ModelChoiceField(
        queryset=Review.objects.none(),
        label='Type d\'examen',
        widget=forms.Select(
            attrs={'id': 'id_review'}),
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date'
    )
    time_slot = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Créneau horaire'
    )
    # profile = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    profile = forms.ModelChoiceField(
        #queryset=take_appointment.userProfile,
        queryset=Profile.objects.all(),
        label='Profile'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialist_name'].queryset = Speciality.objects.none()

        if 'speciality_name' in self.data:
            try:
                specialty_id = int(self.data.get('speciality_name'))
                self.fields['specialist_name'].queryset = Speciality.objects.filter(speciality_name=specialty_id)
                print(self.fields['specialist_name'].queryset)
            except (ValueError, TypeError):
                print('error')
                pass

        # if 'specialist_name' in self.data:
        #    try:
        #        specialist_id = int(self.data.get('specialist_name'))
        #        self.fields['review'].queryset = Review.objects.filter(speciality__id=specialist_id)
        #    except (ValueError, TypeError):
        #        print('error')
        #        pass

    class Meta:
        model = Appointment
        fields = ('speciality_name', 'specialist_name', 'review', 'date', 'time_slot', 'profile',)


class Appointment2Form(AppointmentForm):
    specialist = SpecialityName.objects.all()
    SPECIALITY_CHOICES = []
    for i in specialist:
        SPECIALITY_CHOICES.append((i, i))

    speciality = forms.MultipleChoiceField(
        required=True,
        label='Spécialité',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        choices=SPECIALITY_CHOICES,
    )

    hp = Place.objects.all()
    CITY_CHOICES = []
    for i in hp:
        CITY_CHOICES.append((i, i))

    city = forms.MultipleChoiceField(
        required=True,
        label='Ville',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        choices=CITY_CHOICES,
    )

    typedr = SpecialityName.objects.all()
    SPECIALITY_NAME_CHOICES = []
    for i in typedr:
        SPECIALITY_NAME_CHOICES.append((i, i))

    speciality_name = forms.MultipleChoiceField(
        required=True,
        label='Spécialité',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        choices=SPECIALITY_NAME_CHOICES,
    )

    dr = Speciality.objects.all()
    SPECIALIST_CHOICES = []
    for i in dr:
        SPECIALIST_CHOICES.append((i, i))

    specialist_name = forms.MultipleChoiceField(
        required=True,
        label='Spécialiste',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        choices=SPECIALIST_CHOICES,
    )
    date = forms.SplitDateTimeField(
        label='Date',
        widget=forms.SplitDateTimeWidget(
            date_format='%d/%m/%Y',
            time_format='%H:%M',
            # attrs={'class': 'form-control'}
            date_attrs={'class': 'form-control', 'placeholder': 'JJ/MM/AAAA'},
            time_attrs={'class': 'form-control', 'placeholder': 'HH:MM'},
        )
    )

    TIME_CHOICES = [
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
        ('17:00', '17:00'),
        ('17:30', '17:30'),
        ('18:00', '18:00'),
        ('18:30', '18:30'),
    ]

    time = forms.MultipleChoiceField(
        required=True,
        label='Heure du rendez-vous',
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        choices=TIME_CHOICES,
    )


class CustomAuthForm(AuthenticationForm):
    username = CharField(label='Nom d\'utilisateur :',
                         widget=TextInput(
                             attrs={'class': 'form-control form-control-user', 'placeholder': 'Identifiant'}))
    password = CharField(label='Mot de passe :',
                         widget=PasswordInput(
                             attrs={'class': 'form-control form-control-user', 'placeholder': 'Mot de passe'}))


class AddProfil(Form):
    adresse = CharField(label='Adresse', widget=TextInput(
        attrs={'class': 'form-control RegisterForm', 'placeholder': 'Votre adresse postal'})
                        )
    date_of_birth = DateField(label='Date de naissance :', widget=DateInput(
        attrs={'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': 'JJ/MM/AAAA'}))


class RegisterForm(UserCreationForm):
    username = CharField(label='Nom d\'utilisateur :', widget=TextInput(
        attrs={'class': 'mb-3 mb-sm-0 form-control', 'placeholder': 'Nom d\'utilisateur',
               'id': 'username'}), required=True
                         )
    first_name = CharField(label='Prénom :', widget=TextInput(
        attrs={'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': 'Prénom',
               'id': 'firstname',
               'name': "first_name"}), required=True
                           )
    last_name = CharField(label='Nom de famille :', widget=TextInput(
        attrs={'class': 'col-sm-6 form-control', 'placeholder': 'Nom', 'id': 'lastname',
               'name': "last_name"}), required=True
                          )
    email = EmailField(
        widget=EmailInput(attrs={"class": "form-group form-control", 'placeholder': 'Adresse email',
                                 'id': 'email'}), required=True
    )
    password1 = CharField(max_length=45, label='Mot de passe :', widget=PasswordInput(attrs={
        'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': "Mot de passe",
        'id': 'password1'
    }))
    password2 = CharField(max_length=45, label='Confirmation mot de passe :', widget=PasswordInput(
        attrs={'class': 'col-sm-6 form-control', 'placeholder': "Confirmer votre mot de passe", 'id': 'password2'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        required = ["username", "first_name", "last_name", "email", 'password1', 'password2']

    def first_last_name(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        return last_name, first_name

    def clean_email(self):
        """Permet de verifier si le champ email du formulaire est valide
           si la vérification échoue une erreur de type ValidationError est levé
                      """
        _email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=_email.strip())
            raise ValidationError('L\'adresse email %s est deja utiliser.' % _email.strip())
        except ObjectDoesNotExist:
            return _email
        except MultipleObjectsReturned:
            raise ValidationError('L\'adresse email %s est deja utiliser.' % _email.strip())

    def clean_username(self):
        """Permet de verifier si le champ username du formulaire est valide
           si la vérification échoue une erreur de type ValidationError est levé
                              """
        _username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=_username.strip())
            raise ValidationError('Le pseudo %s est deja utilisé.' % _username.strip())
        except ObjectDoesNotExist:
            return _username


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(label='Ancien mot de passe :',
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control form-control-user', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, label='Nouveau mot de passe :', widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, label='Confirmation du nouveau mot de passe :',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user',
                                                                      'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'email_mismatch': _("The two email addresses fields didn't match."),
        'not_changed': _("The email address is the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=_("Nouvelle adresse email"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=_("Confirmation de la nouvelle adresse email"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user


class EmailChangingForm(EmailChangeForm):
    new_email1 = forms.CharField(label='Nouvelle adresse email :',
                                 widget=forms.EmailInput(
                                     attrs={'class': 'form-control form-control-user', 'type': 'email'}))
    new_email2 = forms.CharField(label='Confirmation de la nouvelle adresse email :',
                                 widget=forms.EmailInput(
                                     attrs={'class': 'form-control form-control-user', 'type': 'email'}))
