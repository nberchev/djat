from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from .forms import RegistrationFrom


def register_user(request, *args, **kwargs):
    user = request.user

    if user.is_authenticated:
        return HttpResponse(f'You are already authenticated as {user.email}.')

    context = {}

    if request.POST:
        form = RegistrationFrom(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            destination = kwargs.get('next')

            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)
