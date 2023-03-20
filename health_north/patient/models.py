from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# from .appointment import Appointment

class TypePlace(models.Model):
    type_place_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Type de lieu"
        verbose_name_plural = "Type de lieux"


class Place(models.Model):
    #cities = models.ForeignKey(Cities, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default="Inconnu")
    type_place = models.ForeignKey(TypePlace, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"


class SpecialityName(models.Model):
    speciality_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Nom de la spécialité"


class Speciality(models.Model):
    speciality_name = models.ForeignKey(SpecialityName, on_delete=models.CASCADE)
    specialist_name = models.CharField(max_length=50)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Spécialiste"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True, blank=True)

    def __repr__(self):
        return 'user %s' % self.user.name

    class Meta:
        verbose_name = "Profil"


class TypeReview(models.Model):
    review_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Type d'examen'"


class Review(models.Model):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    type_review = models.ForeignKey(TypeReview, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Examen"


class Appointment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    specialist_name = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    date = models.DateTimeField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"


class TypeDocument(models.Model):
    type_document_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Type de document"


class Document(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='document')
    create_date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    type_document_name = models.ForeignKey(TypeDocument, on_delete=models.CASCADE)
