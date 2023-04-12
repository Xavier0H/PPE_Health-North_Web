from django.test import TestCase
from django.urls import reverse
from django.utils.dateparse import parse_duration
from django.contrib.auth.models import User
from .models import Region, Department, Cities, Place, Speciality, SpecialityName, Review, TypeReview, Profile, \
    TypePlace, Appointment
from datetime import timedelta

# Create your tests here.

# Index page.

class PatientTest(TestCase):
    def setUp(self) -> None:
        # my_user1 = User.objects.create(username='Testuser1')

        region_code = Region.objects.create(name='Occitanie', code='76', slug='occitanie')
        # code_region = Region.objects.get(code=item["region_code"])
        department = Department.objects.create(name='Haute-Garonne', code='31', slug='haute garonne',
                                               region=region_code)  # 20PB codereg
        toulouse = Cities.objects.create(insee_code='31555', zip_code='31000', name='Toulouse', slug='toulouse',
                                         gps_lat='43.60462560000000', gps_lng='1.44420500000000',
                                         department_code=department)  # 32
        l_union = Cities.objects.create(insee_code='31561', zip_code='31240', name='L\'Union', slug='l union',
                                        gps_lat='43.65102267175571', gps_lng='1.48493496183206',
                                        department_code=department)  # 32

        clinique = TypePlace.objects.create(type_place_name='Clinique')
        laboratoire = TypePlace.objects.create(type_place_name='Laboratoire')
        clinique_toulouse = Place.objects.create(type_place=clinique, cities=toulouse)
        laboratoire_union = Place.objects.create(type_place=laboratoire, cities=l_union)

        medecin = SpecialityName.objects.create(speciality_name='Médecin Généraliste')
        kine = SpecialityName.objects.create(speciality_name='Kinésiste thérapeute')
        cardiologue = SpecialityName.objects.create(speciality_name='Cardiologue')
        dentiste = SpecialityName.objects.create(speciality_name='Dentiste')

        jean_med = Speciality.objects.create(specialist_name='Dr Jean', place=laboratoire_union,
                                             speciality_name=medecin)
        laure_kine = Speciality.objects.create(specialist_name='Mme Laure', place=laboratoire_union,
                                               speciality_name=kine)
        martine_cardio = Speciality.objects.create(specialist_name='Dr Martine', place=clinique_toulouse,
                                                   speciality_name=cardiologue)
        paul_dentiste = Speciality.objects.create(specialist_name='Dr Paul', place=clinique_toulouse,
                                                  speciality_name=dentiste)

        consulation = TypeReview.objects.create(review_name='Consultation')
        analyse = TypeReview.objects.create(review_name='Analyse')
        intervention = TypeReview.objects.create(review_name='Intervention')
        re_education = TypeReview.objects.create(review_name='Ré-éducation')
        massage = TypeReview.objects.create(review_name='Massage')
        chirurgie = TypeReview.objects.create(review_name='Chirurgie')

        delta = timedelta(
            days=50,
            seconds=27,
            microseconds=10,
            milliseconds=29000,
            minutes=5,
            hours=8,
            weeks=2
        )
        vincinq = timedelta(minutes=25)
        quinze = timedelta(minutes=15)
        vingt = timedelta(minutes=20)
        twohours = timedelta(hours=2)
        onehours = timedelta(hours=1)
        trente = timedelta(minutes=30)
        tenhours = timedelta(hours=10)

        consult_jean = Review.objects.create(time=vincinq, speciality=jean_med, type_review=consulation)
        analyse_jean = Review.objects.create(time=quinze, speciality=jean_med, type_review=analyse)
        consult_martine = Review.objects.create(time=vingt, speciality=martine_cardio, type_review=consulation)
        chirurgie_martine = Review.objects.create(time=twohours, speciality=martine_cardio, type_review=chirurgie)
        consult_paul = Review.objects.create(time=trente, speciality=paul_dentiste, type_review=consulation)
        chirurgie_paul = Review.objects.create(time=onehours, speciality=paul_dentiste, type_review=chirurgie)
        massage_laure = Review.objects.create(time=vingt, speciality=laure_kine, type_review=massage)
        reeduc_laure = Review.objects.create(time=trente, speciality=laure_kine, type_review=re_education)

        antoine = User.objects.create(password='BtsSio2023*', username='antoine.dupont', first_name='Antoine',
                                      last_name='Dupont', email='antoine.dupont@bts.com')
        justine = User.objects.create(password='BtsSio2023*', username='justine.ferrari', first_name='Justine',
                                      last_name='Ferrari', email='justine.ferrari@bts.com')

        profil_antoine = Profile.objects.create(adresse='12 rue du pillou 31200 Toulouse', date_of_birth='1986-05-12',
                                                user=antoine)
        profil_justine = Profile.objects.create(adresse='22 chemin de tarbe 31140 Saint-Alban',
                                                date_of_birth='1994-11-06', user=justine)

        Appointment.objects.create(date="2023-03-17 14:30:00+00:00", profile=profil_antoine, specialist_name=jean_med, review=consult_jean)
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow") une region
        # une ville un departement. deux lieux, chaque lieux deux specialiste,chaque specialiste deux examen,
        # les deux examen on des durrer different et elle doivent etre en minutes deux user, deux profile liée au
        # deux user, template prise de rendez-vous soit responsive au mobile

    def test_index_page(self):
        # response = self.client.get(reverse('login'))
        print(Region.objects.all())
        print(Department.objects.all())
        print(Cities.objects.all())
        print(TypePlace.objects.all())
        print(Place.objects.all())
        print(SpecialityName.objects.all())
        print(Speciality.objects.all())
        print(TypeReview.objects.all())
        print(Review.objects.all())
        print(User.objects.all())
        print(Profile.objects.all())
        print(Appointment.objects.all())

    def test_get_appointment_time(self):

        for appointment in Appointment.objects.filter(specialist_name=self.jean_med):
            print(appointment.time)
