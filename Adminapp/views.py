from django.shortcuts import render
from Accounts_app.models import *

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def view_seller(request):
    seller=Seller.objects.all()
    return render(request,'view_seller.html',
                  {'seller':seller})

def view_buyer(request):
    buyer=Buyer.objects.all()
    return render(request,'view_buyer.html',
                  {'buyer':buyer})