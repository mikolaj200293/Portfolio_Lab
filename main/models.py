from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"

# Create your models here.
