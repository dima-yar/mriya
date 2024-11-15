from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/%Y.%m.%d_%H.%M/", default='avatars/default.jpg', null=True, blank=True)


