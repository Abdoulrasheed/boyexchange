from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("buy/<str:currency>/<str:pair>/", views.PairPurchase.as_view(), name="currency_pair_purchase"),
]