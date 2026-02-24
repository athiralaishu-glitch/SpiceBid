from django.urls import path
from Accounts_app import views

urlpatterns=[
    path('registration/',views.registration,name='registration'),
    path('save_register_data/',views.save_register_data,name='save_register_data'),
    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path('buyer_dashboard/',views.buyer_dashboard,name='buyer_dashboard'),
    path('login_user/',views.login_user,name='login_user'),
]