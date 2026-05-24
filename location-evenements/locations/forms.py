from django import forms
from .models import Location
from materiels.models import Materiel
from django.utils import timezone

class LocationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On définit la date minimale à aujourd'hui pour les champs date
        today = timezone.now().date().isoformat()
        self.fields['date_debut'].widget.attrs['min'] = today
        self.fields['date_fin'].widget.attrs['min'] = today
    
    class Meta:
        model = Location
        fields = ['type_evenement', 'date_debut', 'date_fin', 'lieu_evenement', 'notes']
        widgets = {
            'type_evenement': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_evenement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de l\'événement'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes particulières', 'rows': 3}),
        }
