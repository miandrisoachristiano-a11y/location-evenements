from decimal import Decimal
from django.conf import settings
from materiels.models import Materiel

class Cart:
    def __init__(self, request):
        """
        Initialise le panier.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Sauvegarde d'un panier vide dans la session
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, materiel, quantity=1, update_quantity=False):
        """
        Ajoute un matériel au panier ou met à jour sa quantité.
        """
        materiel_id = str(materiel.id)
        if materiel_id not in self.cart:
            self.cart[materiel_id] = {'quantity': 0, 'price': str(materiel.prix_location_jour)}
            
        if update_quantity:
            self.cart[materiel_id]['quantity'] = quantity
        else:
            self.cart[materiel_id]['quantity'] += quantity
            
        self.save()

    def remove(self, materiel):
        """
        Supprime un matériel du panier.
        """
        materiel_id = str(materiel.id)
        if materiel_id in self.cart:
            del self.cart[materiel_id]
            self.save()

    def save(self):
        # Marquer la session comme modifiée pour s'assurer qu'elle est sauvegardée
        self.session.modified = True

    def __iter__(self):
        """
        Itère sur les éléments du panier et récupère les matériels depuis la base de données.
        """
        materiel_ids = self.cart.keys()
        # Obtenir les objets matériels et les ajouter au panier
        materiels = Materiel.objects.filter(id__in=materiel_ids)
        
        cart = self.cart.copy()
        for materiel in materiels:
            cart[str(materiel.id)]['materiel'] = materiel

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Compte tous les éléments dans le panier.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Vider le panier de la session
        del self.session['cart']
        self.save()
