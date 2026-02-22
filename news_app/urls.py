from django .urls import path
from news_app.views import news_list, news_detail

urlpatterns = [
    path('all/', news_list, name='news_list'),
    path('<int:pk>/', news_detail, name='news_detail'),
]