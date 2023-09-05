from django.db import models


# Create your models here.
class Github(models.Model):
    github_user = models.CharField(max_length=1000)
    image_link = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)

    def __str__(self):
        return self.github_user
