from .models import News, Review

def news_and_reviews(request):
    return { "news": News.objects.all(), "reviews": Review.objects.all()}