# is objects that exist in database,
# only model need is profile it will inherit()
# look how any model is defined
# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string
from cloudinary.models import CloudinaryField


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# cre
class MyUser(AbstractUser):
    # User's photo (consider using a library like Django's ImageField for better handling)
    # photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    # not sure how to implement it yet

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )

    name = models.CharField(max_length=200)
    age = models.IntegerField(blank=True, null=True)

    about_you = models.CharField(max_length=200)

    profile_picture = CloudinaryField('profile_picture')

    job = models.CharField(max_length=200)
    place = models.CharField(max_length=200, blank=True, null=True)

    hobbies = models.CharField(max_length=2000, default='')

    languages = models.ManyToManyField(Language)

    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    invite_code_used = models.CharField(max_length=10, blank=True, null=True)

    unique_invite_code = models.CharField(max_length=6, unique=True)

    #
    def __str__(self):
        return self.email


    def save(self, *args, **kwargs):
        if not self.unique_invite_code:
            self.unique_invite_code = generate_unique_code()

            while MyUser.objects.filter(unique_invite_code=self.unique_invite_code).exists():
                self.unique_invite_code = generate_unique_code()

        super(MyUser, self).save(*args, **kwargs)


def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
