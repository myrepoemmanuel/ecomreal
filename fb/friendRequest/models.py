from django.db import models


# Create your models here.

class FriendRequests(models.Model):
    user_one = models.CharField(max_length=200, null=True,blank=True)
    user_two = models.CharField(max_length=200, null=True,blank=True)
    friends = models.BooleanField(default=False)
    state = models.CharField(max_length=200, null=True,blank=True)
    
    def __str__(self):
        return f"{self.id}"
