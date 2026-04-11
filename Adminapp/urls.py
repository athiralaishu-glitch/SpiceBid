from django.urls import path
from Adminapp import views

urlpatterns=[
        path('dashboard/',views.dashboard,name='dashboard'),
        path('',views.admin_login_page,name='admin_login_page'),
        path('admin_login/',views.admin_login,name='admin_login'),
        path('admin_logout/',views.admin_logout,name='admin_logout'),
        path('view_seller/',views.view_seller,name='view_seller'),
        path('view_buyer/',views.view_buyer,name='view_buyer'),
        path('seller_viewmore/<int:s_id>/', views.seller_viewmore, name='seller_viewmore'),
        path('admin/view_winner/', views.view_winner, name='view_winner'),

]