from django.db import models
from django.contrib.auth.models import User

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
    description = models.TextField(max_length=1000, verbose_name="Opis")
    type = models.IntegerField(choices=INSTITUTIONS, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name='Ilość')
    categories = models.ManyToManyField(Category, verbose_name='Kategoria')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=100, verbose_name='Adres')
    phone_number = models.IntegerField(verbose_name='Numer telefonu')
    city = models.CharField(max_length=100, verbose_name='Miasto')
    zip_code = models.CharField(max_length=6, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(verbose_name='Data odbioru')
    pick_up_time = models.TimeField(verbose_name='Godzina odbioru')
    pick_up_comment = models.TextField(max_length=1000, verbose_name='Komentarz')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Użytkownik')

