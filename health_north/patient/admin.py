from django.contrib import admin
from .models import Profile, Document, TypeDocument, SpecialityName, Speciality, Place, TypePlace, Appointment, Review, TypeReview, Region, Department, Cities

# Register your models here.

admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(TypeDocument)
admin.site.register(SpecialityName)
admin.site.register(Speciality)
admin.site.register(Place)
admin.site.register(TypePlace)
admin.site.register(Appointment)
admin.site.register(Review)
admin.site.register(TypeReview)
admin.site.register(Region)
admin.site.register(Department)
admin.site.register(Cities)
