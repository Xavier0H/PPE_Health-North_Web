from django.contrib import admin
from .models import Profile, Document, TypeDocument, SpecialityName, Speciality, Place, TypePlace

# Register your models here.

admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(TypeDocument)
admin.site.register(SpecialityName)
admin.site.register(Speciality)
admin.site.register(Place)
admin.site.register(TypePlace)
