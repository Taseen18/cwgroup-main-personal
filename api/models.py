from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PageView(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"Page view count: {self.count}"

class Hobby(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    status = models.CharField( max_length=10,choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], )

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username} ({self.status})"


class Friends(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)

    def __str__(self):
        return f"Friendship between {self.user1.username} and {self.user2.username}"