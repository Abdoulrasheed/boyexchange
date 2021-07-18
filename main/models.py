from django.db import models
from django.db.models.base import Model
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

class Currency(models.Model):
    name = models.CharField(_("name"), max_length=50)
    short_name = models.CharField(_("short name"), max_length=50)
    logo = models.ImageField(_("logo"), upload_to="logos/")
    reserve = models.FloatField(_("reserve"))
    min_price = models.CharField(_("min to buy"), max_length=50, default=1)
    max_price = models.CharField(_("max to buy"), max_length=50, default=10)
    
    class Meta:
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return self.short_name
    
    def get_logo(self):
        return self.logo.url or ""
    
class ExchangePair(models.Model):
    currency = models.ForeignKey(Currency, verbose_name=_("currency"), on_delete=models.CASCADE)
    pair = models.ForeignKey(Currency, verbose_name=_("pair"), related_name="xchange_pair", on_delete=models.CASCADE)
    pair_equivalent = models.FloatField(_("currency_rate"), default=10, help_text="x number of currency, gives how much of its pair ?")
    
    def __str__(self):
        return f"{self.currency} > {self.pair}" 

class Transaction(models.Model):
    pair = models.ForeignKey(ExchangePair, verbose_name=_("pair"), on_delete=models.CASCADE)
    coin_amount = models.FloatField(_("currency price"))
    pair_amount = models.FloatField(_("pair price"))
    timestamp = models.DateTimeField(_(""), auto_now_add=True)
    transaction_hash = models.CharField(_("transaction hash"), max_length=24)
    has_paid = models.BooleanField(_("paid"), default=False)
    has_mark_paid = models.BooleanField(_("mark paid"), default=False)
    wallet_address = models.CharField(_("wallet"), blank=True, max_length=50)
    bank_name = models.CharField(_("bank name"), blank=True, max_length=50)
    account_name = models.CharField(_("account name"), blank=True, max_length=50)
    account_number= models.CharField(_("account number"), blank=True, max_length=50)
    account_type = models.CharField(_("account type"), blank=True, max_length=50)
    bank_name = models.CharField(_("bank name"), blank=True, max_length=50)
    fullname = models.CharField(_("fullname"), blank=True, max_length=50)
    surname = models.CharField(_("surname"), blank=True, max_length=50)
    email = models.CharField(_("email"), blank=True, max_length=50)
    phone = models.CharField(_("phone"), blank=True, max_length=50)
    
    def __str__(self):
        return f"{self.pair}" 

class Review(models.Model):
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    name = models.CharField(_("name"), max_length=50)
    review = models.CharField(_("review"), max_length=50)
    
    def __str__(self):
        return self.name
    

class News(models.Model):
    title = models.CharField(_("title"), max_length=50)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    body = models.TextField(_("body"))
    
    class Meta:
        verbose_name_plural = "News"
    
    def __str__(self) -> str:
        return self.title

class Config(models.Model):
    btc_wallet_address = models.CharField(_("btc wallet address"), max_length=50)
    eth_wallet_address = models.CharField(_("eth wallet address"), max_length=50)
    usd_wallet_address = models.CharField(_("usd wallet address"), max_length=50)
    account_number = models.CharField(_("bank account number"), max_length=50)
    account_name = models.CharField(_("bank account name"), blank=True, max_length=50)
    bank = models.CharField(_("bank"), max_length=50)
    account_type = models.CharField(_("account type"), max_length=50)