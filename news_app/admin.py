from django.contrib import admin

# Register your models here.
from news_app.models import  News,Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','published_time', 'status']
    list_filter = ['status', 'created_at', 'published_time']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'published_time'
    search_fields = ['title','body']
    ordering = ('-published_time','status')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title']
