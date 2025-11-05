import uuid
from django.db import models
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission


class CustomAccountManager(BaseUserManager):

    def create_superuser(
            self,
            email,
            username,
            first_name='',
            last_name='',
            password=None,
            auth_type='',
            **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields['auth_type'] = auth_type

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(
            email,
            username,
            first_name,
            last_name,
            password,
            **other_fields
        )

    def create_user(
            self,
            email,
            username,
            first_name='',
            last_name='',
            password=None,
            auth_type='',
            **other_fields
    ):
        if not email:
            raise ValueError(lazy('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            auth_type=auth_type,
            **other_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(lazy('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=True, unique=True, blank=True)  # nopep8
    auth_type = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name='newuser_set',
        blank=True,
        help_text=lazy(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='newuser_permissions_set',
        blank=True,
        help_text=lazy('Specific permissions for this user.'),
        related_query_name='newuser',
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username


def default_expiry():
    return now() + timedelta(minutes=5)


class LoginKey(models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)  # nopep8
    created_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=default_expiry)  # nopep8 - 5 min expiry

    def __str__(self):
        return f"{self.user} | {self.expires_at}"

    def is_expired(self):
        return now() > self.expires_at
