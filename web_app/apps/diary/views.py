from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DiaryEntry
from .forms import DiaryEntryForm
from datetime import date

@login_required
def entry_list(request):
    entries = DiaryEntry.objects.filter(user=request.user).order_by('-date', '-created')
    return render(request, 'diary/entry_list.html', {'entries': entries})

@login_required
def entry_create(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.user, request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            form.save_m2m()
            messages.success(request, 'Запись создана')
            return redirect('diary:entry_list')
    else:
        form = DiaryEntryForm(request.user)
    return render(request, 'diary/entry_form.html', {'form': form, 'title': 'Новая запись', 'now': date.today()})

@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DiaryEntryForm(request.user, request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись обновлена')
            return redirect('diary:entry_list')
    else:
        form = DiaryEntryForm(request.user, instance=entry)
    return render(request, 'diary/entry_form.html', {'form': form, 'title': 'Редактирование записи'})

@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(DiaryEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('diary:entry_list')
    return render(request, 'diary/entry_confirm_delete.html', {'entry': entry})