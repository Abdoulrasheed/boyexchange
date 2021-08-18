from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views.generic import ListView
from django.views import View
from django.contrib import sitemaps
from django.urls import reverse
from .models import ExchangePair, Currency, Config, News, Review, Transaction
from .forms import PurchaseForm, TransactionForm

class HomeView(ListView):
    template_name_suffix = "_home"
    model = Currency

class DetailView(View):
    form = PurchaseForm
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            amount_to_send = form.cleaned_data.get("amount_to_send")
            amount_to_receive = form.cleaned_data.get("amount_to_receive")
            coin_to_send = form.cleaned_data.get("coin_to_send")
            coin_to_receive = form.cleaned_data.get("coin_to_receive")
            
            pair = ExchangePair.objects.get(currency=coin_to_send, pair=coin_to_receive)
            
            ctx = {"coin_amount": amount_to_send, "pair_amount": amount_to_receive, "pair": pair}
            return render(request, "main/detail.html", ctx)
        
        return render(request, "main/currency_home.html", { "errors": form.errors })
    
    def get(self, request):
        return redirect("home")

class PairPurchase(View):
    def get(self, request, currency, pair):
        exchanges = ExchangePair.objects.filter(currency__short_name=currency, pair__short_name=pair)
        processing_fee = 0.00055 if pair == "BTC" else 0.0091 if pair == "ETH" else 7.5281 if pair == "USD" else 7102
        
        if exchanges.exists():
            ctx = {
                "processing_fee": processing_fee,
                "exchange": exchanges.first(),
                }
            return render(request, "main/purchase.html", ctx)
        return redirect("home")

class PaymentView(View):
    form = TransactionForm
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            trans = form.save(commit=False)
            trans.transaction_hash = get_random_string(24)
            trans.save()
            
            config = Config.objects.first()
            ctx = { "config": config, "transaction": trans }
            
            if trans.pair.currency.short_name == "NGN":
                ctx['is_naira'] = True
                ctx["transaction_hash"] = trans.transaction_hash
            
            return render(request, "main/payment.html", ctx)
        else:
            return render(request, "main/purchase.html", {"errors": form.errors }) 

class GetPairs(View):
    def get(self, request):
        id = request.GET.get("id")
        currencies = Currency.objects.exclude(id=id).values()
        return JsonResponse({ "currencies": list(currencies) })
        
        
class PairView(View):
    def get(self, request):
        try:
            currency = request.GET.get("currencyIDToSend")
            pair = request.GET.get("currencyIDToReceive")
            exchange_pair = ExchangePair.objects.get(currency__id=currency, pair__id=pair) 
            message = f"Exchange rate: 1 {exchange_pair.currency.short_name} = {exchange_pair.pair_equivalent} {exchange_pair.pair.short_name}"
            return JsonResponse({ "message": message, "rate": exchange_pair.pair_equivalent })
        except:
            return JsonResponse({ "rate": 0 })

class SuccessView(View):
    def get(self, request):
        return render(request, "main/success.html", {})

class DeleteTransaction(View):
    def post(self, request):
        hash = request.POST.get("transaction")
        Transaction.objects.get(transaction_hash=hash).delete()
        return JsonResponse({"success": True})

class MarkPaidView(View):
    def post(self, request):
        hash = request.POST.get("transaction")
        if hash:
            transaction = Transaction.objects.get(transaction_hash=hash)
            transaction.has_mark_paid = True
            transaction.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False})

class ReviewView(ListView):
    model = Review
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        

class NewsView(ListView):
    model = News
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        x = ExchangePair.objects.all()
        return ['home',]

    def location(self, item):
        return reverse(item)