from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail
from django.apps import apps
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager




class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, last_name, first_name, patronymic, job, year_of_birth, department, password, **extra_fields):
        """
        Создать и сохранить Пользователя с полученными логином, ФИО, должностью, отделом и паролем.
        """
        if not username:
            raise ValueError('Логин должен быть указан!')
        if not last_name:
            raise ValueError('Фамилия должна быть указана!')
        if not first_name:
            raise ValueError('Имя должно быть указано!')
        if not patronymic:
            raise ValueError('Отчество должен быть указано или укажите символ прочерка "-"!')
        if not year_of_birth:
            raise ValueError('Год рождения должен быть указан!')
        if not job:
            raise ValueError('Должность должна быть указана!')
        if not department:
            raise ValueError('Отдел должен быть указан!')
        if not password:
            raise ValueError('Пароль должен быть указан!')
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, last_name=last_name, first_name=first_name, patronymic=patronymic,
                          year_of_birth=year_of_birth, job=job, department=department, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, last_name, first_name, patronymic, year_of_birth=None, job=None, department=None,
                    password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, last_name, first_name, patronymic,year_of_birth, job, department, password,
                                 **extra_fields)

    def create_superuser(self, username, last_name, first_name, patronymic, year_of_birth=None, job=None,
                         department=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, last_name, first_name, patronymic, year_of_birth, job, department,
                                 password, **extra_fields)


# from django.contrib.auth.models import User
class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("Логин"),
        max_length=150,
        unique=True,
        help_text=_(
            "Обязательное поле. 150 символов или меньше. Только буквы, цифры и @/./+/-/_."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Пользователь с таким логином уже существует."),
        },
    )
    last_name = models.CharField(_("Фамилия"), max_length=150, blank=False,
                                 help_text=_(
            "Обязательное поле."),)
    first_name = models.CharField(_("Имя"), max_length=150, blank=False,
                                 help_text=_(
            "Обязательное поле."))
    patronymic = models.CharField(_("Отчество"), max_length=150, blank=False,
                                 help_text=_(
            "Обязательное поле."))
    year_of_birth = models.CharField(_("Год рождения"), max_length=4, blank=False, validators=[MinLengthValidator(4)],
                                  help_text=_(
                                      "Обязательное поле. Указывайте год рождения в формате 4 цифр."))
    job = models.CharField(_("Должность"),max_length=300, blank=False,
                                 help_text=_(
            "Обязательное поле."))
    department = models.CharField(_("Отдел"),max_length=200, blank=False,
                                 help_text=_(
            "Обязательное поле."))
    email = models.EmailField(_("Электронная почта"), blank=True)
    is_staff = models.BooleanField(
        _("Доступ к административной части сайта"),
        default=False,
        help_text=_("Определяет, может ли пользователь войти в раздел администрирования."),
    )
    _groups = Group
    _user_permissions = Permission
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Определяет, стоит ли считать пользователя действующим. "
            "Выключите этот параметр вместо удаления пользователя."
        ),
    )
    created_at = models.DateTimeField(_("Дата создания"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['last_name', 'first_name', 'patronymic', 'year_of_birth', 'job', 'department']

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        swappable = "AUTH_USER_MODEL"
        # abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.last_name, self.first_name, self.patronymic)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        short_name = "%s" % (str(self.username))
        return short_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
