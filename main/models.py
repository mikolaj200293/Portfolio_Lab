from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

INSTITUTIONS = (
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna'),
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Institution(models.Model):
    name = models.CharField(max_length=256, verbose_name='Instytucja')
    description = models.TextField(max_length=1000, verbose_name="Opis")
    type = models.IntegerField(choices=INSTITUTIONS, verbose_name="Typ")
    categories = models.ManyToManyField(Category, verbose_name='Kategoria')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Instytucja'
        verbose_name_plural = 'Instytucje'


User_set = settings.AUTH_USER_MODEL


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
    user = models.ForeignKey(User_set, on_delete=models.CASCADE, verbose_name='Użytkownik')

    class Meta:
        verbose_name = 'Darowizna'
        verbose_name_plural = 'Darowizny'

