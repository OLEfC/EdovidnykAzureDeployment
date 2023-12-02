from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.main),
    path('complect/', views.complect),


    path('cpu/', views.main),
    path('complect/gpusearch/', views.gpusearch),
    path('complect/ramsearch/', views.ramsearch),



]
