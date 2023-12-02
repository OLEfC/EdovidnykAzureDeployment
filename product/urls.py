from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/addtowishlist', views.add_to_wishlist),  # новий шлях
    path('<int:product_id>/addtocomparelist', views.add_to_compare),  # новий шлях

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)