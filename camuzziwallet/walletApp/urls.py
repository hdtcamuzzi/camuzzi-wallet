from django.urls import include, path

from . import views

# URLConf for the walletApp application

urlpatterns = [
    path('getwalletinfo/', views.get_wallet_info),
    path('getcards/', views.get_cards),
    path('addcard/', views.add_card),
    path('rmcard/', views.rm_card),
    path('addpurchase/', views.add_purchase),
    path('setlimit/', views.set_limit),
    path('releasecredit/', views.release_credit)
]