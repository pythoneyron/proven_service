from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from apps.accounts.choices import RoleUser


# create user in admin and create superuser in manage.py
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an email address')
        # email = UserManager.normalize_email(email)
        user = self.model(phone_number=phone_number)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password=password)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Пользователи """
    first_name = models.CharField(verbose_name=_('first name'), max_length=30)
    last_name = models.CharField(verbose_name=_('last name'), max_length=30)
    middle_name = models.CharField(verbose_name=_('middle name'),  max_length=255)
    email = models.EmailField(verbose_name=_('E-mail'), max_length=255, unique=True, blank=True, null=True)
    phone_number = models.CharField(verbose_name=_('Номер телефона'), max_length=12, unique=True)
    is_staff = models.BooleanField(verbose_name=_('user status'), default=False,
                                   help_text=_(u"Отметьте, если пользователь может входить"
                                               u" в административную часть сайта."))
    role = models.CharField(verbose_name=_('Роль'), choices=RoleUser.CHOICES, default=RoleUser.User, max_length=3)
    is_active = models.BooleanField(u'Активный', default=False,
                                    help_text=_(u'Отметьте, если пользователь должен считаться активным.'
                                                u' Уберите эту отметку вместо удаления учётной записи.'))
    registration_date = models.DateTimeField(verbose_name=_('registration date'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def get_full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name])

    @staticmethod
    def get_first_letter_in_string(name, dot=None):
        """ Возвращает первую букву строки если она не пустая

        :param unicode str name: принимаемое значение не пустой строки
        :param bool dot: нужна ли точка в конце ? (для инициалов, в них весь сыр-бор)
        """
        letter = ''
        if name:
            letter = next(iter(name))
            if dot and letter:
                letter = letter + '.'
        return letter

    def get_short_last_name(self):
        """ Получение Фимилии И.О. - с инициалами, если они есть """
        return '%s %s%s' % (
            self.last_name,
            self.get_first_letter_in_string(self.first_name, dot=True),
            self.get_first_letter_in_string(self.middle_name, dot=True)
        )

    def get_initial(self):
        return '%s%s' % (
            self.get_first_letter_in_string(self.last_name),
            self.get_first_letter_in_string(self.first_name)
        )

    def get_short_name(self):
        return '%s %s' % (self.last_name, self.first_name)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = u'Пользователя'
        verbose_name_plural = u'Пользователи'
