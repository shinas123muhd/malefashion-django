from django.urls import path
from . import views


urlpatterns = [
    path("", views.storePage, name="store"),
    path(
        "category/<slug:category_slug>/", views.storePage, name="products_by_category"
    ),
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        views.Productdetails,
        name="product_details",
    ),
    path("search/", views.Search, name="search"),
    path(
        "filterprice/<int:min_val>/<int:max_val>/",
        views.filter_price,
        name="filter_price",
    ),
    
    
]
