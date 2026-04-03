from modeltranslation.translator import register, translator, TranslationOptions
from .models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title','body')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)