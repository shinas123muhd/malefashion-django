from django.urls import path
from . import views


urlpatterns = [
    path("adminpanel/", views.AdminPanel, name="adminpanel"),
    path("adminproducts/", views.AdminProducts, name="adminproducts"),
    path("admincategory/", views.AdminCategory, name="admincategory"),
    path("adminorders/", views.AdminOrders, name="adminorders"),
    path("adminusers/", views.AdminUsers, name="adminusers"),
    path("addproduct/", views.AddProduct, name="addproduct"),
    path("blockuser/<int:id>/<str:action>/", views.blockuser, name="blockuser"),
    path("dltproduct/<int:id>/", views.DltProduct, name="dltproduct"),
    path("editproduct/<int:id>/", views.EditProduct, name="editproduct"),
    path("dltcategory/<int:id>/", views.DltCategory, name="dltcategory"),
    path("addcategory/", views.AddCategory, name="addcategory"),
    path("editcategory/<int:id>/", views.EditCategory, name="editcategory"),
    path("orderstatus/<int:id>/<str:action>/", views.OrderStatus, name="orderstatus"),
    path("cancelorder/<int:id>/", views.cancelOrder, name="cancelorder"),
    path("vieworder/<int:id>/", views.viewOrderItems, name="vieworder"),
    path("admincategory/", views.AdminCategory, name="admincategory"),
    path("createcoupon/", views.createcoupon, name="createcoupon"),
    path("coupon/", views.coupon, name="coupon"),
    path("deletecoupon/<int:id>/", views.deletecoupon, name="deletecoupon"),
    path("filterorders/<str:start_date_str>/<str:end_date_str>/", views.filterOrders, name="filterorders"),
    path("adminreport/", views.adminreport, name="adminreport"),
    path("addoffer/", views.addoffer, name="addoffer"),
    path("adminoffers/", views.adminoffers, name="adminoffers"),
    path("deleteoffers/<int:offer_id>/", views.deleteoffers, name="deleteoffers"),
    
    
]
