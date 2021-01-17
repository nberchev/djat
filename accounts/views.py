from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from djat.settings import BASE_URL

from .forms import RegistrationFrom, AccountAuthenticationForm
from .models import Account


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
            destination = get_redirect_if_exists(request)

            if destination:
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form

    return render(request, 'accounts/register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request, *args, **kwargs):
    context = {}

    user = request.user

    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect('home')
        else:
            context['login_form'] = form
    return render(request, 'accounts/login.html', context)


def get_redirect_if_exists(request):
    redirect_page = None

    if request.GET:
        if request.GET.get('next'):
            redirect_page = str(request.GET.get('next'))

    return redirect_page


def account_view(request, *args, **kwargs):
    context = {}

    user_id = kwargs.get('user_id')

    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse('That user does not exist.')

    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        is_self = True
        is_friend = False
        user = request.user

        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = BASE_URL

        return render(request, 'accounts/account.html', context)
