from django.db import models
from django.contrib.auth.models import User

class HabitCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название категории')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name='категория привычек'
        verbose_name_plural='Категории привычек'

    def __str__(self):
        return self.name

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(HabitCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Категория')
    name = models.CharField(max_length=250, verbose_name='Название привычки')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural ='Привычки'
        ordering = ['-created']

    def __str__(self):
        return self.name

class HabitCompletion(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, verbose_name='Привычка')
    date = models.DateField(verbose_name='Дата выполнения')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата отметки')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name='отметка выполнения'
        verbose_name_plural = 'Отметки выполнения'
        ordering = ['-date']
        unique_together = ['habit', 'date']

    def __str__(self):
        return self.date