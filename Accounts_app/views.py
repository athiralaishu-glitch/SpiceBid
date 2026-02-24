from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib import messages

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

        # Create user
        user = CustomUser.objects.create_user(
            username=uname,
            email=email,
            password=pswd,
            role=role,
            is_verified=False
        )

        # Create Seller or Buyer profile
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

            # Role-based redirection
            if user.is_superuser:  # admin/superuser
                return redirect("dashboard") 
            elif user.role == "seller":
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



def buyer_dashboard(request):
    return render(request,'buyer_dashboard.html')


def seller_dashboard(request):
    return render(request,'seller_dashboard.html')