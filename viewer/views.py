from django.shortcuts import render, redirect, get_object_or_404
from .models import Statistic
from faker import Faker


fake = Faker()

def main(request):
    statistic_groups = Statistic.objects.all()
    if request.method == 'POST':
        new_statistic = request.POST.get('new-statistic')
        obj, _ = Statistic.objects.get_or_create(name=new_statistic)
        return redirect('dashboard', obj.slug)
    return render(request, 'main.html', {'statistic_groups': statistic_groups})


def dashboard(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    context = {
        'name': obj.name,
        'slug': obj.slug,
        'data': obj.data,
        'user': request.user.username if request.user.username else fake.name()
    }
    return render(request, 'dashboard.html', context)




