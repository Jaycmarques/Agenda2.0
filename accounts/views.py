# accounts/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from accounts.forms import AccountForm
from .forms import CustomUserCreationForm
from accounts.models import Account
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.views import PasswordResetView


def index(request):
    return render(request, 'accounts/index.html')


@login_required
def home(request):
    accounts = Account.objects.filter(owner=request.user, show=True)
    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'accounts/home.html', context)


@login_required
def search(request):
    search_value = request.GET.get('q', '').strip()
    if search_value == '':
        return redirect('home')

    accounts = Account.objects.filter(owner=request.user, show=True)\
        .filter(
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value) |
            Q(email__icontains=search_value)
    )

    paginator = Paginator(accounts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'accounts/home.html', context)


@login_required
def contact(request, contact_id):
    single_contact = get_object_or_404(
        Account, pk=contact_id, owner=request.user, show=True)
    context = {
        'contact': single_contact,
    }
    return render(request, 'accounts/contact.html', context)


@unauthenticated_user
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('success')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def success(request):
    return render(request, 'accounts/success.html')


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(
                request, "Invalid email or password. Please try again.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


def password_reset(request):
    return render(request, 'accounts/password_reset.html')


@login_required
def create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES)
        email = form.data.get('email')  # Obtém o email do formulário

        # Verifica se já existe um contato com o mesmo e-mail do usuário atual
        if Account.objects.filter(owner=request.user, email=email).exists():
            form.add_error('email', 'Já existe um contato com este e-mail.')
        elif form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('update', contact_id=contact.pk)
    else:
        form = AccountForm()

    return render(request, 'accounts/create.html', {
        'form': form,
        'form_action': reverse('create'),
        'is_update': False
    })


@login_required
def update(request, contact_id):
    contact = get_object_or_404(Account, pk=contact_id, owner=request.user)
    form_action = reverse('update', kwargs={'contact_id': contact_id})

    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact', contact_id=contact.pk)
    else:
        form = AccountForm(instance=contact)

    return render(request, 'accounts/update.html', {'form': form, 'form_action': form_action})


@login_required
def delete(request, contact_id):
    contact = get_object_or_404(Account, pk=contact_id, owner=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('home')

    return render(request, 'accounts/contact.html', {'contact': contact})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
