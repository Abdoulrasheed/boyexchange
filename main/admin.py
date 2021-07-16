from django.contrib import admin
from .models import Currency, ExchangePair

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'price', 'reserve']

class ExhangePairAdmin(admin.ModelAdmin):
    list_display = ['currency', 'pair', 'rate']
    
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangePair, ExhangePairAdmin)

admin.site.site_header = "Boy Exchange Admin"