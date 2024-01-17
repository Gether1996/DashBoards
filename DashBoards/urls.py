from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from viewer.views import main, dashboard, chat_room
from DashBoards.backend_funcs import chart_data

urlpatterns = [
    path('chat/<str:name>/', chat_room, name='chat_room'),
    path('admin/', admin.site.urls),
    path('', main, name='main'),
    path('dashboard/<slug>/', dashboard, name='dashboard'),
    path('dashboard/<slug>/chart/', chart_data, name='chart'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
