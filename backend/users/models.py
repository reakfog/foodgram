from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    '''Custom user class'''
    USER = 'USER'
    ADMIN = 'ADMIN'

    ROLES = (
        (USER, _("User")),
        (ADMIN, _("Administrator")),
    )

    username = models.CharField(
        verbose_name=_("Name"),
        max_length=200,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name=_("Name"),
        max_length=200,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_("Surname"),
        max_length=200,
        blank=False,
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        blank=False, unique=True,
        max_length=254,
    )
    role = models.CharField(
        verbose_name=_("Role"),
        max_length=200,
        choices=ROLES,
        null=False,
        default=USER,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
