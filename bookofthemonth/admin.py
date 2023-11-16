from django.contrib import admin
from .models import BookOfTheMonth


class BookOfTheMonthAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['title']

    def __str__(self):
        return f'{self.title}'

admin.site.register(BookOfTheMonth, BookOfTheMonthAdmin)
