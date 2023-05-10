from django.contrib import admin

# Register your models here.
from .models import Info, Questions

admin.site.register(Info)
admin.site.register(Questions)