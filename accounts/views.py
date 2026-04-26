from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Pillow Housing!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@xframe_options_exempt
def signup_embed(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = render(
                request,
                'accounts/signup_embed.html',
                {
                    'form': SignUpForm(),
                    'success': True,
                    'created_user': user,
                    'beta_site_origin': settings.BETA_SITE_ORIGIN,
                },
            )
            response['Content-Security-Policy'] = (
                f"frame-ancestors 'self' {settings.BETA_SITE_ORIGIN}"
            )
            return response
    else:
        form = SignUpForm()

    response = render(
        request,
        'accounts/signup_embed.html',
        {
            'form': form,
            'success': False,
            'beta_site_origin': settings.BETA_SITE_ORIGIN,
        },
    )
    response['Content-Security-Policy'] = (
        f"frame-ancestors 'self' {settings.BETA_SITE_ORIGIN}"
    )
    return response

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

