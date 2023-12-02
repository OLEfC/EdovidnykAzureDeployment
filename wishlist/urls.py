from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('delete_all', views.delete_all, name='delete_all'),




]
