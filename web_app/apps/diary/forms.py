from django import forms
from .models import DiaryEntry, Emotion, Tag
from datetime import date


class DiaryEntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})  # скрываем стандартный select
    )

    class Meta:
        model = DiaryEntry
        fields = ['date', 'emotion', 'tags', 'title', 'content', 'achievements', 'difficulties', 'tomorrow_plans']
        widgets = {
            'emotion': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок записи'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Что произошло сегодня?'}),
            'achievements': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Что удалось сегодня?'}),
            'difficulties': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'С чем столкнулся?'}),
            'tomorrow_plans': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Что планируешь на завтра?'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['emotion'].queryset = Emotion.objects.filter(is_active=True)
        self.fields['tags'].queryset = Tag.objects.filter(user=user, is_system=False) | Tag.objects.filter(is_system=True)

        # Применяем классы ко всем полям
        for field in self.fields:
            if field != 'tags':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['emotion'].widget.attrs.update({'class': 'form-select'})

        # Настройка поля даты
        if self.instance and self.instance.pk:
            # Редактирование — показываем сохранённую дату
            self.fields['date'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'value': self.instance.date.isoformat()})
        else:
            # Новая запись — сегодняшняя дата
            self.fields['date'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'value': date.today().isoformat()})