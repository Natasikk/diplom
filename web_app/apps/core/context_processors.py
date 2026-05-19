from datetime import date, timedelta
from calendar import monthcalendar
from apps.diary.models import DiaryEntry


def sidebar_data(request):
    if not request.user.is_authenticated:
        return {'calendar_data': [], 'calendar_month': '', 'calendar_year': '', 'calendar_week_days': []}

    today = date.today()
    current_year = today.year
    current_month = today.month

    year = int(request.GET.get('year', current_year))
    month = int(request.GET.get('month', current_month))

    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1

    if year > current_year or (year == current_year and month > current_month):
        year = current_year
        month = current_month

    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    entries = DiaryEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).select_related('emotion')

    calendar_data = []
    month_days = monthcalendar(year, month)
    for week in month_days:
        week_data = []
        for day in week:
            if day != 0:
                current_date = date(year, month, day)
                entry = entries.filter(date=current_date).first()
                emoji = entry.emotion.emoji if entry else ''
                week_data.append({'day': day, 'emoji': emoji})
            else:
                week_data.append({'day': '', 'emoji': ''})
        calendar_data.append(week_data)

    month_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                   'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    week_days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

    prev_month = month - 1
    prev_year = year
    if prev_month < 1:
        prev_month = 12
        prev_year = year - 1

    next_month = month + 1
    next_year = year
    if next_month > 12:
        next_month = 1
        next_year = year + 1

    can_go_forward = (next_year < current_year) or (next_year == current_year and next_month <= current_month)

    return {
        'calendar_data': calendar_data,
        'calendar_month': month_names[month - 1],
        'calendar_year': year,
        'calendar_week_days': week_days,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'can_go_forward': can_go_forward,
        'is_current_month': (year == current_year and month == current_month),
    }