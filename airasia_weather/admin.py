from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.City)
class PersonAdmin(admin.ModelAdmin):
    pass