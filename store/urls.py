from django.urls import path
from .import views


urlpatterns = [
    path('',views.storePage,name='store'),
    path('<slug:category_slug>/',views.storePage,name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.Productdetails,name='product_details'),


]