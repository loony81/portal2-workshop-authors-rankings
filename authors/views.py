from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author
from .forms import AuthorNameForm


def index(request):
    msg = ''
    msg_class = ''

    order_by = request.GET.get('order_by')
    # by default when extracting the authors from the db sort them by the number_of_followers column in descending order
    if not order_by:
        order_by = '-number_of_followers'
    authors_list = Author.objects.order_by(order_by)

    # set the paginator to display 20 authors per page
    items_per_page = 20
    paginator = Paginator(authors_list, items_per_page)
    # check if the form was submitted
    if request.GET.get('search'):
        # search = request.GET.get('search')
        form = AuthorNameForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            # check if author exists in the database
            if Author.objects.filter(nicname=search).exists():
                # get him and find out his position in the ranking
                author = Author.objects.get(nicname=search)
                position = Author.objects.filter(number_of_followers__gt=author.number_of_followers).count()+1
                page = int(position/items_per_page)+1
            else:
                page = 1
                msg = 'Sorry, no author by that name'
    else:
        page = request.GET.get('page', 1)

    # reset the form
    form = AuthorNameForm()

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    context = {
        'authors': authors,
        'order_by': order_by,
        'form': form,
        'message': msg
    }

    return render(request, 'index.html', context)


def keepawake(request):
    return HttpResponse(headers={'Status': 'OK'})
