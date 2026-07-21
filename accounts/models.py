from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    avatar_color = models.CharField(max_length=7, default='#4f46e5')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_initials(self):
        first = self.user.first_name
        last = self.user.last_name
        if first and last:
            return f'{first[0]}{last[0]}'.upper()
        return self.user.username[:2].upper()

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
