from django.shortcuts import get_object_or_404, render
# from .models import
from .utils import get_city_from_ip
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import MyUserCreationForm
from .models import Language
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


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
            login(request, user)  # login reloads, so have store the invite code first
            return redirect('profile')
    else:
        form = MyUserCreationForm()
        invite_code = request.GET.get('invite_code', None)
        request.session['invite_code'] = invite_code
    return render(request, 'register.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:  # if user is not logged in, which should not raise in my project
        return render(request, 'register.html', {'form': MyUserCreationForm()})

    languages = Language.objects.all()

    user_profile = request.user

    if request.method == 'POST':  # handels when the form is submitted for the second time but now with data
        name = request.POST.get('name', None)  # retrives the data and stores in a variable
        age = request.POST.get('age', None)
        profile_picture = request.FILES.get('profile_picture')
        about_you = request.POST.get('about_you', None)
        selected_language_ids = request.POST.getlist('languages', [lang.id for lang in user_profile.languages.all()])
        selected_hobbies = request.POST.get('selectedHobbies', '')
        job = request.POST.get('job', None)
        place = request.POST.get('place', None)
        instagram_url = request.POST.get('instagram_url', None)
        linkedin_url = request.POST.get('linkedin_url', None)

        errors = {}
        if not name:
            errors['name'] = "Name is required."
        elif len(name) < 2 or len(name) > 50:
            errors['name'] = "Name must be between 2 and 50 characters long."
        elif not name.replace(' ', '').isalpha():
            errors['name'] = "Name can only contain alphabetic characters."

        if age is None or age == '':
            user_profile.age = 0
        else:
            try:
                user_profile.age = int(age)
            except ValueError:
                errors['age'] = "Age must be a number."

        if not profile_picture and not user_profile.profile_picture:
            errors['profile_picture'] = "Profile picture is required."

        if 'profile_picture' not in errors and profile_picture:
            user_profile.profile_picture = profile_picture
            user_profile.save()

        if not about_you:
            errors['about_you'] = "Please tell us about yourself."
        elif len(about_you) < 100:
            errors['about_you'] = "Please tell us a bit more about yourself."
        elif len(about_you) > 500:
            errors['about_you'] = "About you must be under 500 characters."

        if not job:
            errors['job'] = "Job field is required."
        elif len(job) < 1:
            errors['job'] = "Job name is too short."
        elif len(job) > 50:
            errors['job'] = "Job name must be under 50 characters."

        if place is not None and len(place) > 50:
            errors['place'] = "Place name must be under 50 characters."

        def validate_url(input_url):  # for URL validation
            if not input_url:
                return True
            validate = URLValidator()
            try:
                validate(input_url)
                return True
            except ValidationError:
                return False

        if not validate_url(instagram_url):
            errors['instagram_url'] = "Invalid URL."
        if not validate_url(linkedin_url):
            errors['linkedin_url'] = "Invalid URL."

        if not errors:
            user_profile.name = name
            user_profile.age = int(age) if age.isdigit() else None
            user_profile.about_you = about_you
            user_profile.job = job
            user_profile.place = place
            user_profile.instagram_url = instagram_url
            user_profile.linkedin_url = linkedin_url
            user_profile.hobbies = selected_hobbies

            user_profile.languages.clear()
            for language_id in selected_language_ids:
                language = Language.objects.get(id=language_id)
                user_profile.languages.add(language)

            user_profile.save()
            return redirect('waitlist')

        context = {'user_profile': user_profile,
                   'errors': errors,
                   'name': name,
                   'age': age,
                   'profile_picture': user_profile.profile_picture,
                   'about_you': about_you,
                   'job': job,
                   'place': place,
                   'instagram_url': instagram_url,
                   'linkedin_url': linkedin_url,
                   'languages': languages,
                   'selected_language_ids': selected_language_ids,
                   'hobbies': selected_hobbies
                   }
        return render(request, 'profile.html', context)

    # for the GET request
    context = {'user_profile': user_profile,
               'name': user_profile.name,
               'age': user_profile.age,
               'profile_picture': user_profile.profile_picture,
               'about_you': user_profile.about_you,
               'job': user_profile.job,
               'place': user_profile.place,
               'instagram_url': user_profile.instagram_url,
               'linkedin_url': user_profile.linkedin_url,
               'languages': languages,
               'selected_language_ids': [lang.id for lang in user_profile.languages.all()],
               'hobbies': user_profile.hobbies
               }
    return render(request, 'profile.html', context)


def waitlist(request):
    return render(request, 'waitlist.html')
