from django import forms
from django.contrib.auth.forms import SetPasswordForm
# from pkg_resources import _
from django.utils.translation import gettext as _
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form, TextInput, DateInput, EmailInput, CharField, EmailField, PasswordInput, DateField


class CustomAuthForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Identifiant'}))
    password = CharField(
        widget=PasswordInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Mot de passe'}))


class AddProfil(Form):
    adresse = CharField(label='Adresse', widget=TextInput(
        attrs={'class': 'form-control RegisterForm', 'placeholder': 'Votre adresse postal'})
                        )
    date_of_birth = DateField(label='Date de naissance :', widget=DateInput(
        attrs={'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': 'JJ/MM/AAAA'}))


class RegisterForm(UserCreationForm):
    username = CharField(widget=TextInput(
        attrs={'class': 'mb-3 mb-sm-0 form-control', 'placeholder': 'Nom d\'utilisateur',
               'id': 'username'}), required=True
    )
    first_name = CharField(widget=TextInput(
        attrs={'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': 'Prénom',
               'id': 'firstname',
               'name': "first_name"}), required=True
    )
    last_name = CharField(widget=TextInput(
        attrs={'class': 'col-sm-6 form-control', 'placeholder': 'Nom', 'id': 'lastname',
               'name': "last_name"}), required=True
    )
    email = EmailField(
        widget=EmailInput(attrs={"class": "form-group form-control", 'placeholder': 'Adresse email',
                                 'id': 'email'}), required=True
    )
    password1 = CharField(max_length=45, widget=PasswordInput(attrs={
        'class': 'col-sm-6 mb-3 mb-sm-0 form-control', 'placeholder': "Mot de passe",
        'id': 'password1'
    }))
    password2 = CharField(max_length=45, widget=PasswordInput(attrs={'class': 'col-sm-6 form-control',
                                                                     'placeholder': "Confirmer votre mot de passe",
                                                                     'id': 'password2'}))

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
           si la vérification échoue une erreur de type ValidationError est lever
                      """
        _email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=_email.strip())
            raise ValidationError('L\'addresse email %s est deja utiliser.' % _email.strip())
        except ObjectDoesNotExist:
            return _email
        except MultipleObjectsReturned:
            raise ValidationError('L\'addresse email %s est deja utiliser.' % _email.strip())

    def clean_username(self):
        """Permet de verifier si le champ username du formulaire est valide
           si la vérification échoue une erreur de type ValidationError est lever
                              """
        _username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=_username.strip())
            raise ValidationError('Le pseudo %s est deja utilisé.' % _username.strip())
        except ObjectDoesNotExist:
            return _username


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-user', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password'}))

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
    # email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'type': 'email'}))
    new_email1 = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'type': 'email'}))
    new_email2 = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-user', 'type': 'email'}))
