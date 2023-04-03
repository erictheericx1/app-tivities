from django.contrib import admin
from .models import User, Activity, UserActivity

# Register your models here.
admin.site.register(Activity)
admin.site.register(UserActivity)