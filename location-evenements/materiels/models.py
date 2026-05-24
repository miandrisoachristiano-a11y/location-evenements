from django.db import models

# Create your models here.

class CategorieMateriel(models.Model):
    nom = models.CharField(max_length=100)  # Vaisselle, Mobilier, Sono...

    def __str__(self):
        return self.nom



class Materiel(models.Model):
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(CategorieMateriel, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    quantite_stock = models.PositiveIntegerField()
    prix_location_jour = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='materiels/', blank=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nom



