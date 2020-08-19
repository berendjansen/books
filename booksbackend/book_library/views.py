from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
import datetime

import pdb

from .models import Book, Author, Publisher
from .bol_scrape import get_information

# Create your views here.


def index(request):
    book_list = Book.objects.order_by('-publication_date')[:25]
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
        'fieldnames' : [f'{f.capitalize()} : {v}' for f, v in book.__iter__()],
        'score_range' : range(1,6),
        'status' : status

    }
    return render(request, 'book_library/detail.html', context)



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

    aut_str = information['authors'].split()
    new_author = Author(first_name=aut_str[0], last_name=' '.join(aut_str[1:]))
    new_author.save()

    new_publisher = Publisher(name=information['publisher'])
    new_publisher.save()

    raw_date = information['publication_date']
    date_digits = ''.join(s for s in raw_date if s.isdigit()).replace(' ', '')
    date_month = ''.join(s for s in raw_date if s.isalpha()).replace(' ', '')

    date_dict = {'januari' : 1,
                 'februari' : 2,
                 'maart' : 3,
                 'april' : 4,
                 'mei' : 5,
                 'juni' : 6,
                 'juli' : 7,
                 'augustus' : 8,
                 'september' : 9,
                 'oktober' : 10,
                 'november' : 11,
                 'december' : 12
                     
    }

    parsed_date = f"{date_digits}-{date_dict[date_month.lower()]}-1"

    try:
        book = get_object_or_404(Book, title=information['title'])
        return HttpResponseRedirect(reverse('book_library:index'))
    except:
    
        new_book = Book(title=information['title'],
                        subtitle=information['subtitle'],
                        publication_date=parsed_date,
                        publisher=new_publisher,
                        pages=information['pages'],
                        EAN=information['EAN'],
                        URL=url,
                        date_added=datetime.datetime.now())

        new_book.save()    
        new_book.authors.add(new_author)
        
        return HttpResponseRedirect(reverse('book_library:index'))
