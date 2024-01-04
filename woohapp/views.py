from django.shortcuts import get_object_or_404, render
# from .models import
from .utils import get_city_from_ip
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import MyUserCreationForm
from .models import MyUser


# view can use a template
# view fires up when something calls a URL
# view typically uses models to access the database and to provide data to templates
# is the only thing that does the job(functioning, the logic)


def home(request):
    invite_code = request.GET.get('invite_code')

    user_ip = request.META.get('REMOTE_ADDR', '')
    user_city = get_city_from_ip(user_ip)
    return render(request, 'home.html', {'user_city': user_city, 'invite_code': invite_code})


def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            invite_code = request.session.get('invite_code', None)
            if invite_code:
                user.invite_code_used = invite_code
                user.save()
            login(request, user)  #login reloads, so have store the invite code first
            return redirect('profile')
    else:
        form = MyUserCreationForm()
        invite_code = request.GET.get('invite_code', None)
        request.session['invite_code'] = invite_code
    return render(request, 'register.html', {'form': form})


def intermediate(request):
    return render(request, 'intermediate.html')


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'register.html', {'form': MyUserCreationForm()})

    try:
        user_profile = MyUser.objects.get(id=request.user.id)
    except MyUser.DoesNotExist:
        user_profile = None

    context = {'user_profile': user_profile}

    return render(request, 'profile.html', context)


def waitlist(request):
    pass
