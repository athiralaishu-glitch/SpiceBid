from django.shortcuts import render,redirect, get_object_or_404
from Accounts_app.models import *
from django.contrib.auth import authenticate,login
from Auction_app.models import  *

# Create your views here.
def dashboard(request):
    return render(request,"dashboard.html")

def admin_login_page(request):
    return render(request,'admin_login.html')
    
def admin_login(request):
    if request.method=='POST':
        uname=request.POST.get("uname")
        pswd=request.POST.get("password")

        if CustomUser.objects.filter(username__contains=uname).exists():
            user=authenticate(username=uname,password=pswd)
            if user is not None:
                login(request,user)
                request.session['username']=uname
                request.session['password']=pswd
                return redirect(dashboard)
            else:
                return redirect(admin_login_page)
        else:
            return redirect(admin_login_page)

def admin_logout(request):
    del request.session['username']
    del request.session['password']
    return redirect(admin_login_page)



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


def view_winner(request):

    auctions = AuctionDB.objects.all()

    for auction in auctions:
        auction.winner = auction.bids.order_by('-amount').first()

    return render(request, "view_winner.html", {
        "auctions": auctions
    })