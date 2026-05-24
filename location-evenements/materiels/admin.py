from django.contrib import admin
from .models import CategorieMateriel, Materiel

@admin.register(CategorieMateriel)
class CategorieMaterielAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Materiel)
class MaterielAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'quantite_stock', 'prix_location_jour', 'disponible')
    list_filter = ('categorie', 'disponible')
    search_fields = ('nom', 'description')
    list_editable = ('quantite_stock', 'prix_location_jour', 'disponible')
