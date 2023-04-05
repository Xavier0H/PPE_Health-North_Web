import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_north.settings')
django.setup()
from patient.models import Region, Department, Cities  # noqa

data = []


def _region():
    with open(f'ressources/regions.json', 'r', encoding="utf8") as txt:
        data = json.loads(txt.read())
        print(data)
        print(type(data))
        for item in data:
            print(item["name"])
            region = Region.objects.create(code=item["code"], name=item["name"], slug=item["slug"])


def _department():
    with open(f'ressources/departments.json', 'r', encoding="utf8") as txt:
        data = json.loads(txt.read())
        print(data)
        print(type(data))
        for item in data:
            print(item["name"])
            code_region = Region.objects.get(code=item["region_code"])
            # print(code_region)
            departement = Department(code=item['code'], name=item["name"], slug=item["slug"], region=code_region)
            print(departement)
            departement.save()


def _cities():
    with open(f'ressources/cities.json', 'r', encoding="utf8") as txt:
        data = json.loads(txt.read())
        print(data)
        print(type(data))
        for item in data:
            print(item["name"])
            code_departement = Department.objects.get(code=item["department_code"])
            # print(code_region)
            cities = Cities(insee_code=item['insee_code'], zip_code=item['zip_code'], name=item["name"],
                            slug=item["slug"], gps_lat=item["gps_lat"], gps_lng=item["gps_lng"],
                            department_code=code_departement)
            # print(cities)
            cities.save()

# _region()
# _department()
# _cities()
