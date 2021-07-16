from django import template
from ..models import ExchangePair

register = template.Library()

@register.simple_tag
def get_rate(currency, pair):
    x = ExchangePair.objects.filter(currency__short_name=currency, pair__short_name=pair)
    return x.first().rate if x.exists() else ""