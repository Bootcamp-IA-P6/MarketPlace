from django.db import models

class MarketPlace(models.Model):
    user = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    password = models.TextField()
    role = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.user