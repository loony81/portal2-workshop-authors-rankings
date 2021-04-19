from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author


def index(request):
    # when extracting the authors from the db sort them  by the number_of_followers column in descending order
    authors_list = Author.objects.order_by('-number_of_followers')
    # set the paginator to display 50 authors per page
    paginator = Paginator(authors_list, 50)
    page = request.GET.get('page', 1)

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'authors': authors})
