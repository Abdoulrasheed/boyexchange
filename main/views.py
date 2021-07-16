from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views.generic import ListView
from django.views import View
from .models import ExchangePair, Currency, Config

class HomeView(ListView):
    template_name_suffix = "_home"
    model = Currency

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PairPurchase(View):
    def get(self, request, currency, pair):
        exchanges = ExchangePair.objects.filter(currency__short_name=currency, pair__short_name=pair)
        if exchanges.exists():
            ctx = {
                "config": Config.objects.first(), 
                "transcode": get_random_string(24),
                "exchange": exchanges.first(),
                }
            return render(request, "main/purchase.html", ctx)
        return redirect("home")