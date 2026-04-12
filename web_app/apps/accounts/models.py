from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата Рождения')
    avatar = models.ImageField(verbose_name='Аватар', upload_to='images/avatars/',
                               default='images/avatars/default.png',
                               validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username