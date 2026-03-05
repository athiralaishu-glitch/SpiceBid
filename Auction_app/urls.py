from django.urls import path
from Auction_app import views

urlpatterns=[
        path('auction_registration/',views.auction_registration,name='auction_registration'),
        path('save_auction/', views.save_auction, name='save_auction'),
        path('auction_detail/<int:auction_id>/', views.auction_detail, name='auction_detail'),
        path('auction/<int:auction_id>/ai-suggest/', views.get_ai_suggestion, name='ai-suggest'),
        path('auction/<int:auction_id>/latest-bid/', views.get_latest_bid, name='latest-bid'),
]