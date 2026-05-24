from django.db import models
from clients.models import Client
from evenements.models import TypeEvenement
from materiels.models import Materiel


class Location(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    type_evenement = models.ForeignKey(TypeEvenement, on_delete=models.SET_NULL, null=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    lieu_evenement = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.type_evenement} ({self.date_debut})"

    @property
    def duree_jours(self):
        return (self.date_fin - self.date_debut).days + 1

    @property
    def total(self):
        return sum(ligne.sous_total for ligne in self.lignes.all())

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ['-date_creation']


class LigneLocation(models.Model):
    location = models.ForeignKey(Location, related_name='lignes', on_delete=models.CASCADE)
    materiel = models.ForeignKey(Materiel, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.materiel} x{self.quantite}"

    @property
    def sous_total(self):
        duree = (self.location.date_fin - self.location.date_debut).days + 1
        return self.quantite * self.prix_unitaire * duree

    class Meta:
        verbose_name = "Ligne de location"
        verbose_name_plural = "Lignes de location"