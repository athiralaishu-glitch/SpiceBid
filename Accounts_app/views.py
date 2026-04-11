from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
from Auction_app.models import *
from Bid_app.models import *
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from Bid_app.models import Bid

from Accounts_app.models import *
from Adminapp import views

# Create your views here.
def registration(request):
    return render(request,'registration.html')

def save_register_data(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        address = request.POST.get("address")
        mobile = request.POST.get("mobile")
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pswd = request.POST.get("password")
        cpswd = request.POST.get("confirm_password")
        role = request.POST.get("role")


        user = CustomUser.objects.create_user(
            username=uname,
            email=email,
            password=pswd,
            role=role,
            is_verified=False
        )


        if role == "seller":
            Seller.objects.create(
                user=user,
                seller_name=name,
                address=address,
                phone_number=mobile
            )

        elif role == "buyer":
            Buyer.objects.create(
                user=user,
                buyer_name=name,
                address=address,
                phone_number=mobile
            )

        return redirect('registration')

    return render(request, "registration.html")

def login_user(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pswd = request.POST.get("password")

        user = authenticate(request, username=uname, password=pswd)

        if user is not None:
            login(request, user)


           
            if user.role == "seller":
                return redirect("seller_dashboard")
            elif user.role == "buyer":
                return redirect("buyer_dashboard")
            else:
                messages.error(request, "User role not recognized!")
                return redirect("registration")
        else:
            messages.error(request, "Invalid username or password")
            return redirect("registration")

    return render(request, "registration.html")

def logout_user(request):
    logout(request)
    messages.success(request,"User Logged out succesfully...")
    return redirect(registration)
    

#-------------------------------------------------------------------------------------------------------------------------------------

def buyer_dashboard(request):
    return render(request,'buyer_dashboard.html')

def about(request):
    return render(request,'about.html')

def active_auctions(request):
    now = timezone.localtime()

    auctions = AuctionDB.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now
    )

    return render(request, "active_auctions.html", {
        "auctions": auctions
    })

def active_auction_viewmore(request, a_id):
    auction = get_object_or_404(AuctionDB, id=a_id)


    now = timezone.localtime()


    is_live = auction.is_live
    highest_bid = auction.bids.order_by('-amount').first()

    if highest_bid:
        current_highest = highest_bid.amount
    else:
        current_highest = auction.starting_price

    return render(request, 'active_auction_viewmore.html', {
        'auction': auction,
        'is_live': is_live,
        'current_highest': current_highest,
        'highest_bid': highest_bid
    })
    
def buyer_past_auctions(request):
    auctions = AuctionDB.objects.filter(
        bids__user=request.user,
        end_time__lt=timezone.now()
    ).distinct()

    return render(request, 'buyer_past_auctions.html', {'auctions': auctions})


def contact(request):
    return render(request, 'contact.html')


@login_required
def buyer_profile(request):
    buyer = Buyer.objects.filter(user=request.user).first()

    return render(request, 'buyer_profile.html', {
        'buyer': buyer
    })


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def seller_my_auctions(request):

    seller = request.user

    auctions = AuctionDB.objects.filter(seller=seller).order_by('-id')

    return render(request, 'seller_auctions.html', {
        'auctions': auctions,
        'now': timezone.now()
    })
    
def past_auction_viewmore(request, a_id):
    auction = get_object_or_404(AuctionDB, id=a_id)
    now = timezone.localtime()
    
    # here we get all bids ordered by highest amount first
    bids = auction.bids.order_by('-amount')
    

    highest_bid = bids.first()
    
    if highest_bid:
        highest_bidder = highest_bid.user
        ended_price = highest_bid.amount
    else:
        highest_bidder = None
        ended_price = None

    return render(request, 'past_auction_viewmore.html', {
        'auction': auction,
        'bids': bids,
        'highest_bid': highest_bid,
        'highest_bidder': highest_bidder,
        'ended_price': ended_price,
        'now': now,
        'is_live': False,
    })






#-----------------------------------------------------------------------------------------------------------------------------------

def save_bid(request, auction_id):
    if request.method == "POST":
        auction = AuctionDB.objects.get(id=auction_id)
        bid_price = Decimal(request.POST.get("bid_price"))

        Bid.objects.create(
            auction=auction,
            user=request.user,
            amount=bid_price
        )

    return redirect("active_auction_viewmore", a_id=auction_id)


#--------------------------------------------------------------------------------------------------------------------------------------
def seller_dashboard(request):
    now = timezone.localtime()
    auctions = AuctionDB.objects.filter(seller=request.user)
    
    total_auctions  = auctions.count()
    active_auctions = auctions.filter(end_time__gt=now, start_time__lte=now).count()
    completed_auctions = auctions.filter(end_time__lt=now).count()
    
    # Total bids received across all auctions

    total_bids = Bid.objects.filter(auction__seller=request.user).count()

    # Recent 3 auctions
    recent_auctions = auctions.order_by('-start_time')[:3]

    return render(request, 'seller_dashboard.html', {
        'total_auctions': total_auctions,
        'active_auctions': active_auctions,
        'completed_auctions': completed_auctions,
        'total_bids': total_bids,
        'recent_auctions': recent_auctions,
        'now': now,
    })

def kyc_form(request):
    return render(request,'kyc_form.html')

def save_kyc(request):

    seller = Seller.objects.get(user=request.user)
    if request.method == "POST":
        

        seller.pan_number = request.POST.get("pan_number")
        seller.pan_card_image = request.FILES.get("pan_card_image")

        seller.aadhar_number = request.POST.get("aadhar_number")
        seller.aadhar_image = request.FILES.get("aadhar_image")

        seller.bank_account_holder_name = request.POST.get("bank_account_holder_name")
        seller.bank_account_number = request.POST.get("bank_account_number")
        seller.bank_ifsc = request.POST.get("bank_ifsc")


        seller.kyc_status = "Pending"

        seller.save()

        messages.success(request, "KYC details submitted successfully. Waiting for admin approval.")
        return redirect("seller_dashboard")

    return render(request, "kyc_form.html")


def seller_account(request):
    seller = Seller.objects.get(user=request.user)
    return render(request,'seller_account.html',
                  {'seller':seller})