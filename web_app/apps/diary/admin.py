from django.contrib import admin
from .models import Emotion, Tag, DiaryEntry

@admin.register(Emotion)
class EmotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created')

@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion', 'title', 'created', 'updated')

