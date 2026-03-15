from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView

from news_app.models import News, Category
from news_app.forms import ContactForm


def news_list(request):
    news_list = News.published.all()
    context = {'news_list': news_list}
    return render(request, 'news/news_list.html', context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.PUBLISHED)
    context = {'news':news}
    return render(request, 'news/news_detail.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:4]
        context['mahalliy_xabarlar']=News.published.all().filter(category__title='Mahalliy').order_by('-published_time')[:5]
        context['xorij_xabarlar']=News.published.all().filter(category__title='Xorij').order_by('-published_time')[:5]
        context['sport_xabarlar']=News.published.all().filter(category__title='Sport').order_by('-published_time')[:5]
        context['texnologiya_xabarlar']=News.published.all().filter(category__title='Texnologiya').order_by('-published_time')[:5]

        return context


###### FUNCTION #######
# def homePageView(request):
#     categories=Category.objects.all()
#     news_list = News.published.all().order_by('-published_time')[:10]
#     local_one = News.published.filter(category__title='Mahalliy').order_by('-published_time')[:1]
#     local_news = News.published.all().filter(category__title='Mahalliy').order_by('-published_time')[1:6]
#     context = {'news_list': news_list,
#                'categories': categories,
#                'local_news': local_news,
#                'local_one': local_one
#                }
#     return render(request, 'news/index.html', context)
#         #### Function ####
# def contactPageView(request):
#     print(request.POST)
#     form = ContactForm(request.POST)
#
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse(' Biz bilan boglanganingiz uchun tashakkur ')
#     context = {'form': form}
#     return render(request, 'news/contact.html', context)
# get ma'lumot olish klientdan
# post jonatish klinetga ma'lumot
#         ##### class ######
class ContactPageView(TemplateView):
    template_name = 'news/contact.html'
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {'form': form}
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('Thank you for contacting us!')
        context = {'form': form}
        return render(request, 'news/contact.html', context)

class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__title='Mahalliy').order_by('-published_time')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__title='Xorij').order_by('-published_time')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__title='Texnologiya').order_by('-published_time')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = News.published.all().filter(category__title='Sport').order_by('-published_time')
        return news





