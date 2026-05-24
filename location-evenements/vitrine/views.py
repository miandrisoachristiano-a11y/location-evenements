from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.urls import reverse
from evenements.models import TypeEvenement
from materiels.models import Materiel, CategorieMateriel
from clients.forms import ClientForm
from clients.models import Client
from locations.forms import LocationForm
from locations.models import Location, LigneLocation
from .cart import Cart


def index(request):
    categoried_id = request.GET.get('categorie')
    if categoried_id:
        materiels = Materiel.objects.filter(categorie_id=categoried_id, disponible=True)
    else:
        materiels = Materiel.objects.filter(disponible=True)
    
    categories = CategorieMateriel.objects.all()
    types_evenements = TypeEvenement.objects.all()
    
    return render(request, 'vitrine/index.html', {
        'materiels': materiels,
        'categories': categories,
        'types_evenements': types_evenements,
        'current_category': int(categoried_id) if categoried_id else None,
    })


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        client_form = ClientForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            messages.success(request, f"Compte créé pour {user.username} ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
    else:
        user_form = UserCreationForm()
        client_form = ClientForm()
    return render(request, 'vitrine/register.html', {
        'user_form': user_form,
        'client_form': client_form
    })


@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('vitrine:admin_dashboard')
    else:
        return redirect('vitrine:user_dashboard')


@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_events = Location.objects.count()
    recent_events = Location.objects.all()[:5]
    return render(request, 'vitrine/admin_dashboard.html', {
        'total_users': total_users,
        'total_events': total_events,
        'recent_events': recent_events
    })


@login_required
def user_dashboard(request):
    client, created = Client.objects.get_or_create(user=request.user)
    my_events = Location.objects.filter(client=client)[:5]
    return render(request, 'vitrine/user_dashboard.html', {
        'my_events': my_events
    })


@staff_member_required
def manage_events(request):
    events = Location.objects.all()
    return render(request, 'vitrine/manage_events.html', {'events': events})


@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, 'vitrine/manage_users.html', {'users': users})


@login_required
def my_events(request):
    client, created = Client.objects.get_or_create(user=request.user)
    events = Location.objects.filter(client=client)
    return render(request, 'vitrine/my_events.html', {'events': events})


@login_required
def profile(request):
    client, created = Client.objects.get_or_create(user=request.user, defaults={
        'nom': request.user.last_name,
        'prenom': request.user.first_name,
        'email': request.user.email
    })
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour !")
            return redirect('vitrine:profile')
    else:
        form = ClientForm(instance=client)
    return render(request, 'vitrine/profile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('vitrine:index')


def admin_login_force(request):
    logout(request)
    return redirect('/accounts/login/?next=/dashboard/')


def materiel_detail(request, pk):
    materiel = get_object_or_404(Materiel, pk=pk)
    return render(request, 'vitrine/detail.html', {'materiel': materiel})


@login_required
def panier_add(request, materiel_id):
    cart = Cart(request)
    materiel = get_object_or_404(Materiel, id=materiel_id)
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        cart.add(materiel=materiel, quantity=quantite, update_quantity=True)
        messages.success(request, f"{materiel.nom} a été ajouté au panier.")
    return redirect('vitrine:panier_detail')

@login_required
def panier_remove(request, materiel_id):
    cart = Cart(request)
    materiel = get_object_or_404(Materiel, id=materiel_id)
    cart.remove(materiel)
    messages.success(request, f"{materiel.nom} a été retiré du panier.")
    return redirect('vitrine:panier_detail')

@login_required
def panier_detail(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            if len(cart) == 0:
                messages.error(request, "Votre panier est vide !")
                return redirect('vitrine:panier_detail')
                
            location = form.save(commit=False)
            client, created = Client.objects.get_or_create(user=request.user)
            location.client = client
            location.save()
            
            # Créer les lignes de location
            for item in cart:
                LigneLocation.objects.create(
                    location=location,
                    materiel=item['materiel'],
                    prix_unitaire=item['price'],
                    quantite=item['quantity']
                )
            
            cart.clear()
            messages.success(request, "Votre demande de réservation a été envoyée avec succès !")
            return redirect('vitrine:my_events')
    else:
        form = LocationForm()
    return render(request, 'vitrine/panier.html', {'cart': cart, 'form': form})


class AdminLoginView(LoginView):
    template_name = 'vitrine/admin_login.html'
    
    def get_success_url(self):
        return reverse('vitrine:dashboard')
