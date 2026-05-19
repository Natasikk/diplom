from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile, created = Profile.objects.update_or_create(
                user=user,
                defaults={
                    'phone': form.cleaned_data.get('phone', ''),
                    'birth_date': form.cleaned_data.get('birth_date')
                }
            )

            login(request, user, backend='apps.accounts.backends.EmailOrUsernameBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if request.POST.get('delete_avatar') == 'true':
            profile.avatar = 'images/avatars/default.png'
            profile.save()
            return redirect('accounts:profile_edit')

        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
    })


@login_required
def profile_delete(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')
    return redirect('accounts:profile')