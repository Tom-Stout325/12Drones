from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
from .forms import *
from weasyprint import HTML



@login_required
def pilot_profile(request):
    profile, created = PilotProfile.objects.get_or_create(user=request.user)
    trainings = profile.trainings.all().order_by('-training_date')

    paginator = Paginator(trainings, 5)  # Show 5 per page
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
            user.is_active = False  # Deactivate until email confirmation
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, 'tom@tom-stout.com', [user.email])
            return render(request, 'registration/activation_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Change this to wherever you want to redirect
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


@login_required
def logout(request):
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')
