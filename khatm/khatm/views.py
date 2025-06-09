from django.shortcuts import redirect
from .models import SurahProgress, AyahAssignment
import os
import json
from django.conf import settings
from django.shortcuts import render, redirect

def load_surah():
    file_path = os.path.join(settings.BASE_DIR, 'static', 'surah', 'anam.json')
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)

def get_next_available_ayah():
    used_numbers = AyahAssignment.objects.values_list('ayah_number', flat=True)
    surah = load_surah()

    for i in range(len(surah)):
        if (i + 1) not in used_numbers:
            return i + 1

    return None

def index(request):
    surah = load_surah()
    progress, _ = SurahProgress.objects.get_or_create(id=1)
    next_ayah_number = get_next_available_ayah()

    if not next_ayah_number:
        AyahAssignment.objects.all().delete()
        progress.completed_count += 1
        progress.save()
        next_ayah_number = get_next_available_ayah()

    AyahAssignment.objects.create(ayah_number=next_ayah_number)

    ayah_data = {
        'number': surah[next_ayah_number - 1]["number"],
        'text': surah[next_ayah_number - 1]["arabic"],
        'translation': surah[next_ayah_number - 1]["translation"]
    }

    context = {
        'ayah': ayah_data,
        'completed_count': progress.completed_count,
    }

    return render(request, 'index.html', context)

def next_ayah(request):
    if request.method == 'POST':
        return redirect('index')
    else:
        return redirect('index')
