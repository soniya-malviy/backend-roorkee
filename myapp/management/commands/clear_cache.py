# myapp/management/commands/clearcache.py

from django.core.management.base import BaseCommand
from django.core.cache import cache
from cacheops import invalidate_all

class Command(BaseCommand):
    help = 'Clear the cache'

    def handle(self, *args, **kwargs):
        cache.clear()
        invalidate_all()
        self.stdout.write(self.style.SUCCESS('Cache cleared successfully'))
