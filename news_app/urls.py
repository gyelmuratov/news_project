from django .urls import path
from news_app.views import (news_list, news_detail, ContactPageView, HomePageView,LocalNewsView,
                           ForeignNewsView,SportNewsView ,TechnologyNewsView)



urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('news/', news_list, name='news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail'),
    path('contact-us/', ContactPageView.as_view(), name='contact'),
    path('local/', LocalNewsView.as_view(), name='local_news'),
    path('foreign/', ForeignNewsView.as_view(), name='foreign_news'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news'),
    path('sport/', SportNewsView.as_view(), name='sport_news'),

]