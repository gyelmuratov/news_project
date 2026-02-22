from django.shortcuts import render, get_object_or_404

from news_app.models import News


# Create your views here.
def news_list(request):
    news_list = News.published.all()
    context = {'news_list': news_list}
    return render(request, 'news/news_list.html', context)

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk, status=News.Status.PUBLISHED)
    context = {'news': news}
    return render(request, 'news/news_detail.html', context)

