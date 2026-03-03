from django.shortcuts import render,redirect, get_object_or_404
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



def seller_viewmore(request, s_id):
    seller = get_object_or_404(Seller, id=s_id)
    if request.method == "POST":
        seller.kyc_status = "Approved"
        seller.save()
        return redirect("seller_viewmore", s_id=s_id)
    return render(request, 'seller_viewmore.html',
                  {'seller': seller})