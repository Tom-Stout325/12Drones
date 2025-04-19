from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import CustomUserCreationForm, PilotProfileForm, TrainingRecordForm
from .models import PilotProfile, TrainingRecord


@login_required
def pilot_profile(request):
    profile, _ = PilotProfile.objects.get_or_create(user=request.user)
    trainings = profile.trainings.all().order_by('-training_date')
    paginator = Paginator(trainings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        profile_form = PilotProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        training_form = TrainingRecordForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
        if training_form.is_valid():
            training = training_form.save(commit=False)
            training.profile = profile
            training.save()
        return redirect('pilot_profile')
    else:
        profile_form = PilotProfileForm(instance=profile, user=request.user)
        training_form = TrainingRecordForm()

    return render(request, 'app/profile.html', {
        'profile_form': profile_form,
        'training_form': training_form,
        'profile': profile,
        'page_obj': page_obj,
    })


@login_required
def delete_training(request, pk):
    training = get_object_or_404(TrainingRecord, pk=pk, profile__user=request.user)
    training.delete()
    return redirect('pilot_profile')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('pilot_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def permission_denied_view(request, exception=None):
    return render(request, 'registration/login_required.html', status=403)

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)
