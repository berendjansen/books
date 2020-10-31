from django.urls import path

from . import views

app_name = 'book_library'
urlpatterns = [
    path('', views.index, name="index"),
    path('all_books', views.all_books, name="all_books"),
    path('wishlist', views.wishlist, name="wishlist"),
    path('finished_reading', views.finished_reading, name="finished_reading"),
    path('<int:book_id>/', views.detail, name='detail'),
    path('<int:book_id>/rate/', views.rate, name='rate'),
    path('<int:book_id>/change_status/', views.change_status, name='change_status'),
    path('add_book', views.add_book, name="add_book"),
    path('search_book', views.search_book, name="search_book"),
    # path('search_results', views.search_results, name="search_results"),
    path('author/<int:author_id>/', views.author_page, name='author_page'),
]

