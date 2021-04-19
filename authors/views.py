from django.shortcuts import render
from django.http import HttpResponse
from .models import Author


def index(request):
    authors = Author.objects.order_by('-number_of_followers')
    return render(request, 'index.html', {'authors': authors})
