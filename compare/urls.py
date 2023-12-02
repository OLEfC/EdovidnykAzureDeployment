from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.compare_view, name='wishlist'),
    path('delete_<str:table_type>/', views.delete_table, name='delete_table'),


    #path('delete_cpu', views.cpu, name='delete_item'),
    #path('delete_all', views.delete_all, name='delete_all'),




]
