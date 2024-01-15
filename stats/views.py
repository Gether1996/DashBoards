from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic, DataItem
from faker import Faker
from django.http import JsonResponse
from django.db.models import Sum

fake = Faker()

def main(request):
    qs = Statistic.objects.all()
    if request.method == 'POST':
        new_statistic = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_statistic)
        return redirect('dashboard', obj.slug)
    return render(request, 'main.html', {'qs': qs})

def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    context = {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    }
    return render(request, 'dashboard.html', context)

def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x['value__sum'] for x in qs]
    chart_labels = [x['owner'] for x in qs]
    return JsonResponse({
        'chartData': chart_data,
        'chartLabels': chart_labels
    })
