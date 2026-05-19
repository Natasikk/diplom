from django.shortcuts import render
from apps.diary.models import DiaryEntry
from apps.habits.models import Habit, HabitCompletion
from datetime import date, timedelta


def home(request):
    context = {}
    if request.user.is_authenticated:
        context['diary_count'] = DiaryEntry.objects.filter(user=request.user).count()
        context['habits_count'] = Habit.objects.filter(user=request.user, is_active=True).count()

        today = date.today()

        diary_streak = 0
        has_today = DiaryEntry.objects.filter(user=request.user, date=today).exists()

        if has_today:
            current_date = today
        else:
            current_date = today - timedelta(days=1)

        while True:
            if DiaryEntry.objects.filter(user=request.user, date=current_date).exists():
                diary_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        context['diary_streak'] = diary_streak

        habit_streak = 0
        has_today_habit = HabitCompletion.objects.filter(habit__user=request.user, date=today).exists()

        if has_today_habit:
            current_date = today
        else:
            current_date = today - timedelta(days=1)

        while True:
            if HabitCompletion.objects.filter(habit__user=request.user, date=current_date).exists():
                habit_streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        context['habit_streak'] = habit_streak

    return render(request, 'home.html', context)
