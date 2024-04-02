from django.db import models
from api.accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length = 255)

    def __str__(self) -> str:
        return self.name
    


class News(models.Model):
    title = models.CharField(max_length = 255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
   

    def __str__(self):
        return self.title
    

