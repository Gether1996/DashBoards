from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from stats.views import main, dashboard, chart_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('<slug>/', dashboard, name='dashboard'),
    path('<slug>/chart/', chart_data, name='chart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)