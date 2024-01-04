from django.conf import settings
from django.core.cache import cache

from catalog.models import Category


def get_categories():
    categories = cache.get('categories')
    if categories is None:
        categories = Category.objects.all()
        cache.set('categories', categories, 60)

    return categories
