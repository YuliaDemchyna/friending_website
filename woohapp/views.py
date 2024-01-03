from django.shortcuts import get_object_or_404, render
# from .models import
from .utils import get_city_from_ip
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import MyUserCreationForm
from models import MyUser


# view can use a template
# view fires up when something calls a URL
# view typically uses models to access the database and to provide data to templates
# is the only thing that does the job(functioning, the logic)


def home(request):
    invite_code = request.GET.get('invite_code')
    if invite_code:
        request.session['invite_code'] = invite_code
    user_ip = request.META.get('REMOTE_ADDR', '')
    user_city = get_city_from_ip(user_ip)
    context = {'user_city': user_city}
    return render(request, 'home.html', context)


def register(request):
    print(request.method)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})


def intermediate(request):
    return render(request, 'intermediate.html')


def profile(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            # Try to retrieve user's existing data
            try:
                user_data = MyUser.objects.get(user=request.user)
                form = MyUser(instance=user_data)  # Pre-fill the form with existing data
            except MyUser.DoesNotExist:
                form = YourForm()  # If no data exists, provide an empty form
    else:
        return return render(request, 'register.html', {'form': form})
    return render(request, 'waitlist.html')


def waitlist(request):
    pass
