from django.shortcuts import render
from django.http import HttpResponse
from .models import Author


def index(request):
    authors = Author.objects.all()
    return render(request, 'index.html', {'authors': authors})
