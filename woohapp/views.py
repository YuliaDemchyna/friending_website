from django.shortcuts import get_object_or_404, render
# from .models import
from .utils import get_city_from_ip

# view can use a template
# view fires up when something calls a URL
# view typically uses models to access the database and to provide data to templates
# is the only thing that does the job(functioning, the logic)


def home(request):
    user_ip = request.META.get('REMOTE_ADDR', '')  # Get user's IP address
    user_city = get_city_from_ip(user_ip)

    # Pass the city to the template
    context = {'user_city': user_city}
    return render(request, 'home.html', context)  # define home in templates folder


def join(request):
    return render(request, 'join.html', {})
