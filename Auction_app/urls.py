from django.urls import path
from Auction_app import views

urlpatterns=[
        path('auction_registration/',views.auction_registration,name='auction_registration'),
        path('save_auction/', views.save_auction, name='save_auction'),

]