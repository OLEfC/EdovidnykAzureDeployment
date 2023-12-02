"""
URL configuration for edovidnyk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Додайте цей імпорт

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),  # Додайте цей рядок
    path('main/', include('main.urls')),  # Додайте цей рядок
    path('wishlist/', include('wishlist.urls')),  # Додайте цей рядок
    path('usereditprofile/', include('usereditprofile.urls')),  # Додайте цей рядок
    path('shop/', include('shopmap.urls')),  # Додайте цей рядок
    path('search/', include('search.urls')),  # Додайте цей рядок
    path('faq/', include('faq.urls')),  # Додайте цей рядок
    path('product/', include('product.urls')),  # Додайте цей рядок
    path('compare/', include('compare.urls')),  # Додайте цей рядок








]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

