from django.db import models
from django.db.models.base import Model
from django.utils.translation import ugettext_lazy as _

class Currency(models.Model):
    name = models.CharField(_("name"), max_length=50)
    price = models.FloatField(_("price"), default=0)
    short_name = models.CharField(_("short name"), max_length=50)
    logo = models.ImageField(_("logo"), upload_to="logos/")
    reserve = models.FloatField(_("reserve"))
    
    class Meta:
        verbose_name_plural = "Currencies"
    
    def __str__(self):
        return self.short_name
    
    def get_logo(self):
        return self.logo.url or ""
    

class ExchangePair(models.Model):
    currency = models.ForeignKey(Currency, verbose_name=_("currency"), on_delete=models.CASCADE)
    pair = models.ForeignKey(Currency, verbose_name=_("pair"), related_name="xchange_pair", on_delete=models.CASCADE)
    rate = models.CharField(_("rate"), max_length=50)
    
    def __str__(self):
        return f"{self.currency} > {self.pair}" 

class Config(models.Model):
    btc_wallet_address = models.CharField(_("btc wallet address"), max_length=50)
    eth_wallet_address = models.CharField(_("eth wallet address"), max_length=50)
    usd_wallet_address = models.CharField(_("usd wallet address"), max_length=50)
    account_no = models.CharField(_("bank account number"), max_length=50)
    bank = models.CharField(_("bank"), max_length=50)
    account_type = models.CharField(_("account type"), max_length=50)