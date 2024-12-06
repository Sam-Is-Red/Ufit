from django.db import models
from django.contrib.auth.models import User


# from django.contrib.auth.models import AbstractUser
# from django.utils.timezone import now
# Create your models here.
class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ##topic = modles.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    description = models.TextField(null=True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-update", "-created"]

    def str(self):
        return self.title


# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    host = models.CharField(max_length=200)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class Author(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# Extend User model for different roles
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('organization', 'Wellness Organization'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.user.username
