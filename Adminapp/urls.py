from django.urls import path
from Adminapp import views

urlpatterns=[
        path('dashboard/',views.dashboard,name='dashboard'),
        path('view_seller/',views.view_seller,name='view_seller'),
        path('view_buyer/',views.view_buyer,name='view_buyer'),

]