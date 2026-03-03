from django.shortcuts import render,redirect
from Auction_app.models import *

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