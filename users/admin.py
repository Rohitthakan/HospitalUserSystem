from django.contrib import admin
from users.models import UserProfileInfo, Blog, Picture, Appointment

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Picture)
admin.site.register(Blog)
admin.site.register(Appointment)
