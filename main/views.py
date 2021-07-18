from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.crypto import get_random_string
from django.views.generic import ListView
from django.views import View
from django.contrib import sitemaps
from django.urls import reverse
from .models import ExchangePair, Currency, Config, News, Review, Transaction
from .forms import TransactionForm

class HomeView(ListView):
    template_name_suffix = "_home"
    model = Currency

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.all().order_by('-pk')[:2]
        context['transactions'] = transactions
        return context

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
            ctx = { 
                   "config": config, 
                   "transaction": trans,
                }
            
            if trans.pair.currency.short_name == "NGN":
                ctx['is_naira'] = True
                ctx["transaction_hash"] = trans.transaction_hash
            
            return render(request, "main/payment.html", ctx)
        else:
            return render(request, "main/purchase.html", {"errors": form.errors }) 

class PairView(View):
    def post(self, request):
        try:
            exchange_pk = request.POST.get("exchange")
            amount = request.POST.get("amount")
            amount = float(amount)
            action = request.POST.get("action")
            exchange = ExchangePair.objects.get(pk=exchange_pk) 
            
            if action == "send":
                rate =  exchange.pair_equivalent * amount
            else:
                exchange = ExchangePair.objects.get(currency__name=exchange.pair.name, pair__name=exchange.currency.name) 
                rate = exchange.pair_equivalent * amount
                
            return JsonResponse({ "rate": rate, "name": exchange.currency.short_name })
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
        tran_id = request.POST.get("transaction")
        if tran_id:
            transaction = Transaction.objects.get(pk=tran_id)
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