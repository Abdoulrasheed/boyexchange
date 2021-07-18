from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("get_pair_rate/", views.PairView.as_view(), name="get_pair_rate"),
    path("payment/", views.PaymentView.as_view(), name="payment"),
    path("mark_paid/", views.MarkPaidView.as_view(), name="mark_paid"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("reviews/", views.ReviewView.as_view(), name="reviews"),
    path("news/", views.NewsView.as_view(), name="news"),
    path("delete_transaction/", views.DeleteTransaction.as_view(), name="delete_transaction"),
    path("buy/<str:currency>/<str:pair>/", views.PairPurchase.as_view(), name="currency_pair_purchase"),
]