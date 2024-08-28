from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Nexly.urls')),  # Incluye las rutas de Nexly
]
