from datetime import date, timedelta
from calendar import monthcalendar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Habit, HabitCompletion, HabitCategory
from .forms import HabitForm


@login_required
def habit_list(request):
    month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                   'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    habits = Habit.objects.filter(user=request.user, is_active=True)

    # Поиск по названию
    search_name = request.GET.get('search_name', '')
    if search_name:
        habits = habits.filter(name__icontains=search_name)

    # Фильтр по категориям
    categories = request.GET.getlist('categories')
    if categories:
        habits = habits.filter(category__id__in=categories)

    today = date.today()
    current_year = int(request.GET.get('year', today.year))
    current_month = int(request.GET.get('month', today.month))

    if current_month < 1:
        current_month = 12
        current_year -= 1
    elif current_month > 12:
        current_month = 1
        current_year += 1

    habits_data = []
    for habit in habits:
        start_date = date(current_year, current_month, 1)
        if current_month == 12:
            end_date = date(current_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(current_year, current_month + 1, 1) - timedelta(days=1)

        completions = HabitCompletion.objects.filter(
            habit=habit,
            date__gte=start_date,
            date__lte=end_date
        )
        completions_by_day = {completion.date.day: completion for completion in completions}

        month_days = monthcalendar(current_year, current_month)
        calendar_data = []
        for week in month_days:
            week_data = []
            for day in week:
                if day != 0:
                    current_date = date(current_year, current_month, day)
                    completion = completions_by_day.get(day)
                    is_completed = completion is not None
                    can_check = current_date <= today
                    week_data.append({
                        'day': day,
                        'completed': is_completed,
                        'can_check': can_check,
                        'comment': completion.comment if completion else '',
                        'date_str': f"{current_year}-{current_month:02d}-{day:02d}"
                    })
                else:
                    week_data.append({'day': '', 'completed': False, 'can_check': False, 'comment': '', 'date_str': ''})
            calendar_data.append(week_data)

        prev_month = current_month - 1
        prev_year = current_year
        if prev_month < 1:
            prev_month = 12
            prev_year = current_year - 1

        next_month = current_month + 1
        next_year = current_year
        if next_month > 12:
            next_month = 1
            next_year = current_year + 1

        can_go_forward = (next_year < today.year) or (next_year == today.year and next_month <= today.month)

        habits_data.append({
            'habit': habit,
            'calendar_data': calendar_data,
            'current_month': current_month,
            'current_month_name': month_names[current_month - 1],
            'current_year': current_year,
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
            'can_go_forward': can_go_forward,
        })

    all_categories = HabitCategory.objects.filter(is_active=True)
    selected_categories = [int(c) for c in categories] if categories else []

    context = {
        'habits_data': habits_data,
        'week_days': week_days,
        'search_name': search_name,
        'all_categories': all_categories,
        'selected_categories': selected_categories,
    }
    return render(request, 'habits/habit_list.html', context)


@login_required
def toggle_habit_ajax(request):
    if request.method == 'POST':
        habit_id = request.POST.get('habit_id')
        date_str = request.POST.get('date')
        checked = request.POST.get('checked') == 'true'
        comment = request.POST.get('comment', '')

        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        target_date = date.fromisoformat(date_str)
        today = date.today()

        if target_date > today:
            return JsonResponse({'error': 'Нельзя отмечать будущие дни'}, status=400)

        if checked:
            HabitCompletion.objects.update_or_create(
                habit=habit,
                date=target_date,
                defaults={'comment': comment}
            )
        else:
            HabitCompletion.objects.filter(habit=habit, date=target_date).delete()

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def habit_create(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
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
            return redirect('habits:habit_list')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Редактирование привычки'})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.delete()
    return redirect('habits:habit_list')