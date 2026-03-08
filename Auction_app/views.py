from django.shortcuts import render,redirect
from Auction_app.models import *
from Auction_app.ai_suggestion import suggest_next_bid_openrouter
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import get_object_or_404





# Create your views here.
def auction_registration(request):
    return render(request,'auction_reg.html')

def save_auction(request):
    if request.method == "POST":
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
    auction = AuctionDB.objects.get(id=auction_id)
    current_bid = auction.ended_price or auction.starting_price
    suggested_bid = suggest_next_bid_openrouter(current_bid, min_increment=10)
    return render(request, "active_auction_viewmore.html", {"auction": auction, "suggested_bid": suggested_bid})

logger = logging.getLogger(__name__)
@login_required
def get_ai_suggestion(request, auction_id):
    try:
        auction = AuctionDB.objects.get(id=auction_id)
    except AuctionDB.DoesNotExist:
        return JsonResponse({"error": "Auction not found."}, status=404)

    #  Auction not live
    if not auction.is_live:
        return JsonResponse({"error": "Auction is not live."}, status=400)

    # Get REAL highest bid
    highest_bid = auction.bids.order_by('-amount').first()

    if highest_bid:
        current_bid = highest_bid.amount
    else:
        current_bid = auction.starting_price

    # Dynamic percentage-based increment (2%)
    min_increment = max(int(current_bid * Decimal("0.02")), 100)

    # Clean rounded suggestion
    base_suggestion = current_bid + min_increment
    base_suggestion = round(base_suggestion / 100) * 100

    # Get user & auction history
    user = request.user

    user_past_bids = list(
        auction.bids.filter(user=user).values_list('amount', flat=True)
    )

    auction_history = list(
        auction.bids.values('user__username', 'amount')
    )

    # Ask AI (optional intelligent adjustment)
    suggested_bid = suggest_next_bid_openrouter(
        current_bid=current_bid,
        min_increment=min_increment,
        auction_history=auction_history,
        user_behavior=user_past_bids
    )

    #  Fallback if AI fails
    if not suggested_bid:
        suggested_bid = base_suggestion

    #  Ensure suggestion is always above current bid
    try:
        suggested_bid = int(float(suggested_bid))
    except:
        suggested_bid = base_suggestion

    if suggested_bid <= current_bid:
        suggested_bid = base_suggestion

    return JsonResponse({
        "suggested_bid": suggested_bid
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
