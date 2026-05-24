from django.contrib import admin
from .models import Location, LigneLocation

class LigneLocationInline(admin.TabularInline):
    model = LigneLocation
    extra = 1

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'type_evenement', 'date_debut', 'date_fin', 'statut', 'total')
    list_filter = ('statut', 'type_evenement', 'date_debut')
    search_fields = ('client__nom', 'client__prenom', 'lieu_evenement')
    inlines = [LigneLocationInline]
    
    readonly_fields = ('date_creation',)
