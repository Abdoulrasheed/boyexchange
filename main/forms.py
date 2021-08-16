from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['timestamp', 'transaction_hash']

class PurchaseForm(forms.Form):
    amount_to_send = forms.IntegerField()
    amount_to_receive = forms.IntegerField()
    coin_to_send = forms.CharField(max_length=100)
    coin_to_receive = forms.CharField(max_length=100)
    