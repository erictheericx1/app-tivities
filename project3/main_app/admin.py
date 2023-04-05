from django.contrib import admin
from .models import AppUser, Activity, UserActivity, Inter

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Activity)
admin.site.register(UserActivity)
admin.site.register(Inter)