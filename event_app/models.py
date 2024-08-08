from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import AbstractUser


   
class Event(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phoneno = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=255, default='Pending')
    event_confirmation = models.CharField(max_length=255, default='Pending')
    def __str__(self):
        return self.name

#class Event(models.Model):
    name = models.CharField(max_length=255)
    event_type = models.CharField(max_length=255, default='default_value')
    phoneno = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.CharField(max_length=255, default='default_value')
    payment_status = models.CharField(max_length=255, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    event_confirmation = models.CharField(max_length=255, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.date}"

class CustomUser(AbstractUser):
    # add custom fields if needed
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        related_query_name='customuser',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=10)
    # Add more fields as needed


class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Add more fields as needed

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    

class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='feedback_set')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"