from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.models import HitCountMixin
from hitcount.templatetags.hitcount_tags import get_hit_count
from hitcount.utils import get_hitcount_model
from hitcount.models import HitCount
from hitcount.views import HitCountMixin


from news_app.models import News, Category
from news_app.forms import ContactForm, CommentForm
from news_project.custom_permissions import OnlyLoggedSuperUser


def news_list(request):
    news_list = News.published.all()
    context = {'news_list': news_list}
    return render(request, 'news/news_list.html', context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.PUBLISHED)

    # HitCount
    hit_count = HitCount.objects.get_for_object(news)
    HitCountMixin.hit_count(request, hit_count)

    # Kommentlar
    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        'news': news,
        'total_hits': hit_count.hits,
        'comments': comments,
        'comment_count': comment_count,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
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

@login_required
def homePageView(request):
    categories=Category.objects.all()
    news_list = News.published.all().order_by('-published_time')[:10]
    local_one = News.published.filter(category__title='Mahalliy').order_by('-published_time')[:1]
    local_news = News.published.all().filter(category__title='Mahalliy').order_by('-published_time')[1:6]
    context = {'news_list': news_list,
               'categories': categories,
               'local_news': local_news,
               'local_one': local_one
               }
    return render(request, 'news/index.html', context)
        #### Function ####
def contactPageView(request):
    print(request.POST)
    form = ContactForm(request.POST)

    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponse(' Biz bilan boglanganingiz uchun tashakkur ')
    context = {'form': form}
    return render(request, 'news/contact.html', context)
#get ma'lumot olish klientdan
#post jonatish klientga ma'lumot
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

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status',)

    template_name = 'crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home')

class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status',)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {'admin_users': admin_users}
    return render(request, 'pages/admin_page.html', context)


class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_results.html'
    context_object_name = 'barcha yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))













