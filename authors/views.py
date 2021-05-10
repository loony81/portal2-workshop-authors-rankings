from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author


def index(request):
    order_by = request.GET.get('order_by')
    # by default when extracting the authors from the db sort them by the number_of_followers column in descending order
    if not order_by:
        order_by = '-number_of_followers'
    authors_list = Author.objects.order_by(order_by)

    # set the paginator to display 50 authors per page
    paginator = Paginator(authors_list, 50)
    page = request.GET.get('page', 1)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'authors': authors, 'order_by': order_by})


def keepalive(request):
    return HttpResponse(headers={'Status': 'OK'})
