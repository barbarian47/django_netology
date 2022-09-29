from django.shortcuts import render
from django.core.paginator import Paginator

from books.models import Book


def books_view(request):
    books = Book.objects.all()
    template = 'books/books_list.html'
    context = {'books': books}

    return render(request, template, context)


def book(request, date):
    books = Book.objects.filter(pub_date=date)
    previous_date = Book.objects.filter(pub_date__lt=date).first()
    next_date = Book.objects.filter(pub_date__gt=date).first()
    template = 'books/books_list.html'
    context = {
        'books': books,
        'previous_date': previous_date.pub_date if previous_date else None,
        'next_date': next_date.pub_date if next_date else None
    }

    return render(request, template, context)
