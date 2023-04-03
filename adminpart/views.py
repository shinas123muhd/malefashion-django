from django.shortcuts import render


# Create your views here.
def AdminPanel(request):
    
    return render(request,'admin/adminpanel.html')
def AdminUsers(request):
    return render(request,'admin/adminusers.html')
def AdminProducts(request):
    return render(request,'admin/adminproducts.html')
def AdminOrders(request):
    return render(request,'admin/adminorders.html')