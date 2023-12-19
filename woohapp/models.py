# is objects that exist in database,
# only model need is profile it will inherit()
# look how any model is defined
# Create your models here.

from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # Linking UserProfile to Django's built-in User model for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # User's photo (consider using a library like Django's ImageField for better handling)
    # photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    # not sure how to implement it yet

    # Job and Place
    job = models.CharField(max_length=200)
    place = models.CharField(max_length=200, blank=True, null=True)

    # Personality Traits
    trait_one = models.CharField(max_length=50)
    trait_two = models.CharField(max_length=50)
    trait_three = models.CharField(max_length=50)

    # Languages
    languages = models.ManyToManyField(Language)
#     # Social Accounts
#     instagram_url = models.URLField(blank=True, null=True)
#     linkedin_url = models.URLField(blank=True, null=True)
#
#     # Invitation Code Used by the User
#     invite_code_used = models.CharField(max_length=10, blank=True, null=True)
#
#     # User's Unique Invite Code
#     unique_invite_code = models.CharField(max_length=6, unique=True)
#
#     def __str__(self):
#         return self.user.username
#
#     # not sure how to do this
#     def save(self, *args, **kwargs):
#         # Code to generate unique_invite_code
#         # Ensure the code is unique before saving
#         if not self.unique_invite_code:
#             self.unique_invite_code = generate_unique_code()
#         super(UserProfile, self).save(*args, **kwargs)
#
#
# # Example function to generate unique invite codes
# def generate_unique_code():
#     # Implement logic to generate a unique 6-character code
#     pass
