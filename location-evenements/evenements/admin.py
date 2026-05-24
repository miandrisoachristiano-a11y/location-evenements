from django.contrib import admin
from .models import TypeEvenement

@admin.register(TypeEvenement)
class TypeEvenementAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)
