from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import Habit, HabitCompletion, HabitCategory
from .forms import HabitForm, HabitCompletionForm


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user, is_active=True)
    return render(request, 'habits/habit_list.html', {'habits': habits})


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            messages.success(request, 'Привычка создана')
            return redirect('habits:habit_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Новая привычка'})


@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Привычка обновлена')
            return redirect('habits:habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Редактирование привычки'})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Привычка удалена')
        return redirect('habits:habit_list')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})


@login_required
def habit_today(request):
    today = date.today()
    habits = Habit.objects.filter(user=request.user, is_active=True)

    completions = {}
    for habit in habits:
        try:
            completion = HabitCompletion.objects.get(habit=habit, date=today)
            completions[habit.id] = {'completed': True, 'comment': completion.comment}
        except HabitCompletion.DoesNotExist:
            completions[habit.id] = {'completed': False, 'comment': ''}

    if request.method == 'POST':
        # Получаем список всех отмеченных привычек
        checked_habit_ids = request.POST.getlist('habit_id')

        # Для всех привычек пользователя
        for habit in habits:
            completion = HabitCompletion.objects.filter(habit=habit, date=today)
            if str(habit.id) in checked_habit_ids:
                # Если отмечено, но записи нет — создаём
                if not completion.exists():
                    HabitCompletion.objects.create(habit=habit, date=today, comment='')
                    messages.success(request, f'Отмечено: "{habit.name}"')
            else:
                # Если не отмечено, но запись есть — удаляем
                if completion.exists():
                    completion.delete()
                    messages.success(request, f'Отметка снята: "{habit.name}"')

        return redirect('habits:habit_today')

    return render(request, 'habits/habit_today.html', {
        'habits': habits,
        'completions': completions,
        'today': today
    })