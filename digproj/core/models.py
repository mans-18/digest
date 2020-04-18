from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                    PermissionsMixin
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # Only email and passwd! No 'name'
    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Kollege(models.Model):
    """Equipe to be used for a Persona"""
    name = models.CharField(max_length=255)
    # Instead of referencing User directly, set the 1st arg (model) by settings
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    crm = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Event(models.Model):
    """Event to occur to a persona"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    start = models.DateTimeField()
    color = models.CharField(max_length=20, blank=True)
    insurance = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start']


class Persona(models.Model):
    """Persona model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    street = models.CharField(max_length=255, blank=True)
    complement = models.CharField(max_length=100, blank=True)
    postalcode = models.CharField(max_length=20, blank=True)
    dob = models.DateField(null=True, blank=True)
    registerdate = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=255, blank=True)
    kollegen = models.ManyToManyField('Kollege')
    events = models.ManyToManyField('Event')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
