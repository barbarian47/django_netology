from django.contrib import admin
from phones.models import Phone

# Register your models here.
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
