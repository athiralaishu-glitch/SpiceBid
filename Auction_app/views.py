from django.shortcuts import render

# Create your views here.
def auction_registration(request):
    return render(request,'auction_reg.html')