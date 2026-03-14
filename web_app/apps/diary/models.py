from django.db import models
from django.contrib.auth.models import User

class Emotion(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название эмоции')
    emoji = models.CharField(max_length=10, verbose_name='Эмодзи')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name='эмоция'
        verbose_name_plural = 'Эмоции'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название тега')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Пользователь')
    is_system = models.BooleanField(default=False, verbose_name='Системный тег')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name='тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    date = models.DateField(verbose_name='Дата')
    emotion = models.ForeignKey(Emotion, on_delete=models.CASCADE, verbose_name='Настроение дня')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги дня')
    title = models.CharField(max_length=200, default='Без названия', verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание записи')
    achievements = models.TextField(blank=True, null=True, verbose_name='Достижения дня')
    difficulties = models.TextField(blank=True, null=True, verbose_name='Трудности дня')
    tomorrow_plans = models.TextField(blank=True, null=True, verbose_name='Планы на завтра')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата и время обновления')

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'Записи'
        ordering = ['-date', '-created']

    def __str__(self):
        date_str = self.date.strftime("%d.%m.%Y")
        title = self.title
        return f"{date_str} - {title}"
