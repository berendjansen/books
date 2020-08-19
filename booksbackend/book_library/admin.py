from django.contrib import admin

from .models import Book, Author, Publisher

# admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Author)

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'get_authors', 'read', 'in_possession', 'on_wishlist')
    list_filter = ['title', 'publication_date', 'date_added']
    search_fields = ['title']

admin.site.register(Book, BookAdmin)
