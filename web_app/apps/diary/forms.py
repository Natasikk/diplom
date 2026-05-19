from django import forms
from .models import DiaryEntry, Emotion, Tag
from datetime import date

class DiaryEntryForm(forms.ModelForm):
    emotion = forms.ModelChoiceField(
        queryset=Emotion.objects.filter(is_active=True),
        widget=forms.RadioSelect,
        required=True,
        label='Настроение дня'
    )

    class Meta:
        model = DiaryEntry
        fields = ['date', 'emotion', 'tags', 'title', 'content', 'achievements', 'difficulties', 'tomorrow_plans']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок записи'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Что произошло сегодня?'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(user=user, is_system=False) | Tag.objects.filter(is_system=True)

        for field in self.fields:
            if field not in ['emotion', 'tags']:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

        today = date.today()
        if self.instance and self.instance.pk:
            self.fields['date'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'value': self.instance.date.isoformat(), 'max': today.isoformat()}
            )
        else:
            self.fields['date'].widget = forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control', 'value': today.isoformat(), 'max': today.isoformat()}
            )