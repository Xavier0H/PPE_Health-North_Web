from django.test import TestCase
from django.urls import reverse
from .models import Region, Department, Cities, Place, Speciality, Review, TypeReview, Profile, User


# Create your tests here.

# Index page.

class PatientTest(TestCase):
    def setUp(self) -> None:
        # my_user1 = User.objects.create(username='Testuser1')

        region_code = Region.objects.create(name='Occitanie', code='76', slug='occitanie')
        # code_region = Region.objects.get(code=item["region_code"])
        department = Department.objects.create(name='Haute-Garonne', code='31', slug='haute garonne', region=region_code)  # 20PB codereg
        Cities.objects.create(insee_code='31555', zip_code='31000', name='Toulouse', slug='toulouse',
                              gps_lat='43.60462560000000', gps_lng='1.44420500000000', department_code=department) #32

        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow") une region
        # une ville un departement. deux lieux, chaque lieux deux specialiste,chaque specialiste deux examen,
        # les deux examain on des durrer different et elle doivent etre en minutes deux user, deux profile liée au
        # deux user, template prise de rendez-vous soit responsive au mobile


    def test_index_page(self):
        # response = self.client.get(reverse('login'))
        print(Cities.objects.all())
        pass
