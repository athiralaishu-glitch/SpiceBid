from django.shortcuts import render,redirect
from Auction_app.models import *
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import get_object_or_404
from Bid_app.models import *
from .suggestion import calculate_suggested_bid



# Create your views here.
def auction_registration(request):
    seller = Seller.objects.filter(user=request.user).first()

    kyc_status = seller.kyc_status if seller else "pending"

    return render(request, 'auction_reg.html', {
        "kyc_status": kyc_status
    })

def save_auction(request):
    if request.method == "POST":

        seller = Seller.objects.get(user=request.user)
        if seller.kyc_status != "approved":
            return redirect("seller_dashboard")

        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_price = request.POST.get("starting_price")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        image = request.FILES.get("image")

        AuctionDB.objects.create(
            seller=request.user,
            title=title,
            description=description,
            starting_price=starting_price,
            start_time=start_time,
            end_time=end_time,
            image=image
        )

        return redirect("seller_dashboard")

    return redirect("auction_registration")


def edit_auction(request, auction_id):
    auction = get_object_or_404(AuctionDB, id=auction_id, seller=request.user)
    if request.method == "POST":
        auction.title = request.POST.get("title")
        auction.description = request.POST.get("description")
        auction.starting_price = request.POST.get("starting_price")
        auction.start_time = request.POST.get("start_time")
        auction.end_time = request.POST.get("end_time")
        if request.FILES.get("image"):
            auction.image = request.FILES.get("image")
        auction.save()
        return redirect("seller_auctions")
    return render(request, "edit_auction.html", {"auction": auction})

def delete_auction(request, auction_id):
    auction = get_object_or_404(AuctionDB, id=auction_id, seller=request.user)
    if request.method == "POST":
        auction.delete()
        return redirect("seller_auctions")
    return redirect("seller_auctions")

def auction_detail(request, auction_id):
    auction = get_object_or_404(AuctionDB, id=auction_id)

    current_bid = auction.ended_price or auction.starting_price
    suggested_bid = calculate_suggested_bid(current_bid)

    return render(request, "active_auction_viewmore.html", {
        "auction": auction,
        "current_bid": current_bid,
        "suggested_bid": suggested_bid
    })


@login_required
def get_bid_suggestion(request, auction_id):
    try:
        auction = AuctionDB.objects.get(id=auction_id)
    except AuctionDB.DoesNotExist:
        return JsonResponse({"error": "Auction not found."}, status=404)

    if not auction.is_live:
        return JsonResponse({"error": "Auction is not live."}, status=400)

    highest_bid = auction.bids.order_by('-amount').first()

    if highest_bid:
        current_bid = highest_bid.amount
    else:
        current_bid = auction.starting_price

    suggested_bid = calculate_suggested_bid(current_bid)

    return JsonResponse({
        "suggested_bid": int(suggested_bid)
    })


def get_latest_bid(request, auction_id):
    try:
        auction = AuctionDB.objects.get(id=auction_id)
    except AuctionDB.DoesNotExist:
        return JsonResponse({"error": "Auction not found."}, status=404)

    highest_bid = auction.bids.select_related('user').order_by('-amount').first()
    return JsonResponse({
        "highest_bid": highest_bid.amount if highest_bid else auction.starting_price,
        "bidder": highest_bid.user.username if highest_bid else None
    })

