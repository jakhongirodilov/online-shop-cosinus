from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CustomUserChangeForm, AddressForm
from .models import Address


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


def logout_view(request):
    logout(request)
    
    return redirect('home')


def profile(request):
    user = request.user
    addresses = Address.objects.filter(user=user)

    return render(request, 'profile.html', {'user':user, 'addresses':addresses})


def edit_profile(request):
    user = request.user 

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

        return redirect('profile')
    else:
        form = CustomUserChangeForm(instance = user)

    return render(request, 'edit_profile.html', {'form':form})


def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
        
    context = {
        'form':form
    }
    return render(request, 'add_address.html', context)
