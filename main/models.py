from django.db import models

INSTITUTIONS = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
)


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"


class Institution(models.Model):
    name = models.CharField(max_length=256, verbose_name='Instytucja')
    description = models.TextField(verbose_name="Opis")
    type = models.IntegerField(choices=INSTITUTIONS, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"
# Create your models here.
