from django.contrib import admin

from .models import Book, Author, Publisher


admin.site.register(Publisher)

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author', 'read', 'in_possession', 'on_wishlist')
    list_filter = ['title', 'publication_date', 'date_added']
    search_fields = ['title']

admin.site.register(Book, BookAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    list_filter = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

admin.site.register(Author, AuthorAdmin)
