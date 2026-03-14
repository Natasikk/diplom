from django.contrib import admin
from .models import HabitCategory, Habit, HabitCompletion

@admin.register(HabitCategory)
class HabitCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created')

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created', 'updated')

@admin.register(HabitCompletion)
class HabitCompletionAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'created', 'updated')