from django.http import JsonResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from viewer.models import Statistic
import secrets


def chart_data(request, slug):
    obj = get_object_or_404(Statistic, slug=slug)
    qs = obj.data.values('owner').annotate(Sum('value'))
    chart_data = [x['value__sum'] for x in qs]
    chart_labels = [x['owner'] for x in qs]
    return JsonResponse({
        'chartData': chart_data,
        'chartLabels': chart_labels
    })


def generate_random_color():
    # Generate random bytes for the RGB components
    random_bytes = secrets.token_bytes(3)

    # Convert the bytes to hexadecimal and concatenate them
    color_code = "#" + random_bytes.hex()

    return color_code