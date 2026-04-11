from django.urls import path
from Accounts_app import views

urlpatterns=[
    path('registration/',views.registration,name='registration'),
    path('save_register_data/',views.save_register_data,name='save_register_data'),

    path('seller_dashboard/',views.seller_dashboard,name='seller_dashboard'),
    path('about/', views.about, name='about'),
    path('active_auctions/', views.active_auctions, name='active_auctions'),
    path('active_auction_viewmore/<int:a_id>/', views.active_auction_viewmore, name='active_auction_viewmore'),
    path('seller_auctions/', views.seller_my_auctions, name='seller_auctions'),
    path('past_auction_viewmore/<int:a_id>/', views.past_auction_viewmore, name='past_auction_viewmore'),
    

    path('save_bid/<int:auction_id>/', views.save_bid, name='save_bid'),

    path('buyer_dashboard/',views.buyer_dashboard,name='buyer_dashboard'),
    path('login_user/',views.login_user,name='login_user'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('kyc_form/',views.kyc_form,name='kyc_form'),
    path('save_kyc/',views.save_kyc,name='save_kyc'),
    path('seller_account/',views.seller_account,name='seller_account'),
    path('buyer_past_auctions/', views.buyer_past_auctions, name='buyer_past_auctions'),
    path('contact/', views.contact, name='contact'),
    path('buyer_profile/', views.buyer_profile, name='buyer_profile'),
]