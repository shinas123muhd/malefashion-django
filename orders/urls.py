from . import views
from django.urls import path

urlpatterns=[
    path('place_order/',views.PlaceOrder,name='placeorder'),
    
]