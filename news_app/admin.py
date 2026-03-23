from django.contrib import admin

# Register your models here.
from news_app.models import News, Category, Contact, Comment


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

admin.site.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created_time','active']
    list_filter = ['active', 'created_time']
    search_fields = ['user', 'body']
    actions = ['disable_comments','activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)


