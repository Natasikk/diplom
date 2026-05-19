from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DiaryEntry, Emotion, Tag
from .forms import DiaryEntryForm
from datetime import date
from django.db.models import Q


@login_required
def entry_list(request):
    entries = DiaryEntry.objects.filter(user=request.user)

    search_title = request.GET.get('search_title', '')
    if search_title:
        entries = entries.filter(title__icontains=search_title)

    search_date = request.GET.get('search_date', '')
    if search_date:
        entries = entries.filter(date=search_date)

    emotions = request.GET.getlist('emotions')
    if emotions:
        entries = entries.filter(emotion__id__in=emotions)

    tags = request.GET.getlist('tags')
    if tags:
        entries = entries.filter(tags__id__in=tags).distinct()

    entries = entries.order_by('-date', '-created').distinct()

    all_emotions = Emotion.objects.filter(is_active=True)
    all_tags = Tag.objects.filter(Q(user=request.user) | Q(is_system=True)).distinct()

    context = {
        'entries': entries,
        'all_emotions': all_emotions,
        'all_tags': all_tags,
        'selected_emotions': [int(e) for e in emotions],
        'selected_tags': [int(t) for t in tags],
        'search_title': search_title,
        'search_date': search_date,
    }

    return render(request, 'diary/entry_list.html', context)


@login_required
def entry_create(request):
    emotions = Emotion.objects.filter(is_active=True)
    tags = Tag.objects.filter(user=request.user, is_system=False) | Tag.objects.filter(is_system=True)

    if request.method == 'POST':
        form = DiaryEntryForm(request.user, request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user

            achievements_list = request.POST.getlist('achievements')
            difficulties_list = request.POST.getlist('difficulties')
            plans_list = request.POST.getlist('tomorrow_plans')

            entry.achievements = '\n'.join([a for a in achievements_list if a.strip()]) if achievements_list else ''
            entry.difficulties = '\n'.join([d for d in difficulties_list if d.strip()]) if difficulties_list else ''
            entry.tomorrow_plans = '\n'.join([p for p in plans_list if p.strip()]) if plans_list else ''

            entry.save()
            form.save_m2m()
            return redirect('diary:entry_list')
    else:
        form = DiaryEntryForm(request.user)
    return render(request, 'diary/entry_form.html', {
        'form': form,
        'title': 'Новая запись',
        'now': date.today(),
        'emotions': emotions,
        'all_tags': tags
    })


@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    emotions = Emotion.objects.filter(is_active=True)
    tags = Tag.objects.filter(user=request.user, is_system=False) | Tag.objects.filter(is_system=True)

    if request.method == 'POST':
        form = DiaryEntryForm(request.user, request.POST, instance=entry)
        if form.is_valid():
            achievements_list = request.POST.getlist('achievements')
            difficulties_list = request.POST.getlist('difficulties')
            plans_list = request.POST.getlist('tomorrow_plans')

            entry.achievements = '\n'.join([a for a in achievements_list if a.strip()]) if achievements_list else ''
            entry.difficulties = '\n'.join([d for d in difficulties_list if d.strip()]) if difficulties_list else ''
            entry.tomorrow_plans = '\n'.join([p for p in plans_list if p.strip()]) if plans_list else ''

            form.save()
            return redirect('diary:entry_list')
    else:
        form = DiaryEntryForm(request.user, instance=entry)
    return render(request, 'diary/entry_form.html', {
        'form': form,
        'title': 'Редактирование записи',
        'now': date.today(),
        'emotions': emotions,
        'all_tags': tags
    })


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    entry.delete()
    return redirect('diary:entry_list')


@login_required
def entry_detail(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    return render(request, 'diary/entry_detail.html', {'entry': entry})