from django.contrib import admin
from .models import Currency, ExchangePair, Review, News, Transaction, Config

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'reserve']

class ExhangePairAdmin(admin.ModelAdmin):
    list_display = ['currency', 'pair', 'pair_equivalent']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'review']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['pair', 'coin_amount', 'pair_amount']
    readonly_fields = ['pair', 'coin_amount', 'pair_amount', 'transaction_hash', 'has_mark_paid', 'wallet_address', 'bank_name', 'account_name', 'account_type', 'account_number', 'fullname', 'email', 'phone']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']

admin.site.register(Config)
admin.site.register(News, NewsAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Review, ReviewAdmin)    
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangePair, ExhangePairAdmin)

admin.site.site_header = "Boy Exchange Admin"