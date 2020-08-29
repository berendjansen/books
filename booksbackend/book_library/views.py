from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.db.models import Q

import datetime

import pdb

from .models import Book, Author, Publisher
from .bol_scrape import get_information

# Create your views here.


def index(request):
    book_list = Book.objects.order_by('-date_added')[:25]
    latest_wish_list = Book.objects.filter(on_wishlist=True).order_by('-date_added')[:10]
    
    latest_finished_list = Book.objects.filter(read=True).order_by('-date_read')[:10]

    context = {'book_list' : book_list,
               'wish_list' : latest_wish_list,
               'finished_list' : latest_finished_list,}
    
    return render(request, 'book_library/index.html', context)

def all_books(request):
    book_list = Book.objects.order_by('-publication_date')
    context = {'book_list' : book_list,}
    return render(request, 'book_library/all_books.html', context)

def wishlist(request):
    wishlist = Book.objects.filter(on_wishlist=True).order_by('-date_added')
    context = {'wishlist' : wishlist,}
    return render(request, 'book_library/wishlist.html', context)

def finished_reading(request):
    finished_list = Book.objects.filter(read=True).order_by('-date_added')
    context = {'finished_list' : finished_list,}
    return render(request, 'book_library/finished_reading.html', context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.on_wishlist:
        status = 'On wishlist'
    elif book.read:
        status = 'Finished reading'
    elif book.in_possession:

        if book.reading:
            status = "Currently Reading"
        else:
            status = 'Acquired'


    context = {
        'book' : book,
        'author' : book.author,
        'fieldnames' : [f'{f.capitalize()} : {v}' for f, v in book.__iter__()],
        'score_range' : range(1,6),
        'status' : status

    }
    return render(request, 'book_library/detail.html', context)

def author_page(request, author_id):
    author = get_object_or_404(Author, pk=author_id)

    book_list = Book.objects.filter(author__id=author.id)
    
    print(book_list)
    context = {
        'author' : author,
        'book_list' : book_list,
    }
    
    return render(request, 'book_library/author_page.html', context)

def rate(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    given_score = request.POST['score']

    book.score = given_score
    book.save()
    
    return HttpResponseRedirect(reverse('book_library:detail', args=(book.id,)))

def change_status(request, book_id):
    book = get_object_or_404(Book, pk=book_id)


    new_status = request.POST.get('status')

    if new_status == 'On wishlist':
        book.on_wishlist = 1
        book.read = 0
        book.reading = 0
        book.in_possession = 0
    elif new_status == 'In possession':
        book.on_wishlist = 0
        book.in_possession = 1
        book.read = 0
        book.date_acquired = datetime.datetime.now()
    elif new_status == 'Read':
        book.on_wishlist = 0
        book.in_possession = 1
        book.reading = 0
        book.read = 1
        book.date_read = datetime.datetime.now()
    elif new_status == 'Currently reading':
        book.on_wishlist = 0
        book.in_possession = 1
        book.reading = 1
        book.read = 0
        book.date_started_reading = datetime.datetime.now()

    book.save()
    
    return HttpResponseRedirect(reverse('book_library:detail', args=(book.id,)))

def add_book(request):
    url = request.POST['add_book']

    information = get_information(url)

    try:
        book = get_object_or_404(Book, title=information['title'])
        return HttpResponseRedirect(reverse('book_library:index'))
    except:
        aut_str = information['author'].split()
        new_author = Author(first_name=aut_str[0], last_name=' '.join(aut_str[1:]))
        new_author.save()

        publisher = Publisher.objects.filter(name=information['publisher'])

        if not publisher:
            new_publisher = Publisher(name=information['publisher'])
            new_publisher.save()
            publisher = new_publisher
        else:
            publisher = publisher[0]
        
        new_book = Book(title=information['title'],
                        author=new_author,
                        subtitle=information['subtitle'],
                        publication_date=information['publication_date'],
                        publisher=publisher,
                        # pages=information['pages'],
                        isbn=information['isbn'],
                        URL=url,
                        date_added=datetime.datetime.now())

        new_book.save()    
        # new_book.authors.add(new_author)
        
        return HttpResponseRedirect(reverse('book_library:index'))



def search_book(request):
    query = request.GET['search_book']

    query_results = Book.objects.filter(
        Q(title__icontains=query) | Q(authors__first_name__icontains=query) | Q(authors__last_name__icontains=query))
    
    
    context = {
        'query': query,
        'query_results' : query_results,
    }
    
    return render(request, 'book_library/search_results.html', context)

