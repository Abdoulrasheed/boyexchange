from .models import News, Review, Transaction, Currency

def news_and_reviews(request):
    transactions = Transaction.objects.all().order_by('-pk')[:10]
    return { "coins":  Currency.objects.all(), "news": News.objects.all(), "reviews": Review.objects.all(), "transactions": transactions}