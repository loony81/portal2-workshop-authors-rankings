from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Author, UpdateDate
from .forms import AuthorNameForm


# set the paginator to display 20 authors per page
items_per_page = 20
last_updated = UpdateDate.objects.get(model_name='Author')

def calculate_page(author):
    position = Author.objects.filter(number_of_followers__gt=author.number_of_followers).count() + 1
    # there could be other authors with the same number of followers
    same_number_of_followers = Author.objects.filter(number_of_followers=author.number_of_followers).count()
    if same_number_of_followers > 1:
        # if there are, then get all of them and recalculate the position
        authors_with_the_same_number_of_followers = Author.objects.filter(
            number_of_followers=author.number_of_followers).order_by('id')
        for i in range(same_number_of_followers):
            if authors_with_the_same_number_of_followers[i].nicname == author.nicname:
                break
            position += 1
    page = position / items_per_page
    if page.is_integer():
        page = int(page)
    else:
        page = int(page) + 1
    return page



def index(request):
    msg = ''
    anchor = ''

    order_by = request.GET.get('order_by')
    # by default when extracting the authors from the db sort them by the number_of_followers column in descending order
    # and then by id for those authors who have the same number of followers
    if not order_by:
        order_by = '-number_of_followers'
    authors_list = Author.objects.order_by(order_by, 'id')
    paginator = Paginator(authors_list, items_per_page)
    # check if the form was submitted
    if request.GET.get('search'):
        form = AuthorNameForm(request.GET) # bind the form
        if form.is_valid():
            name = form.cleaned_data['search']
            # check if author exists in the database
            if Author.objects.filter(nicname=name).exists():
                # how many authors with the same name?
                number_of_authors = Author.objects.filter(nicname=name).count()
                if number_of_authors > 1:
                    # if there are more than one author with the same name, get the one with the most number of followers
                    author = Author.objects.filter(nicname=name).order_by('-number_of_followers').first()
                else:
                    author = Author.objects.get(nicname=name)
                # find out his position in the ranking and the page
                page = calculate_page(author)
                # anchor will allow the page to start at a certain point so that the author's position is inside the viewport
                anchor = author.nicname
            else:
                page = 1
                msg = 'Sorry, no author by that name'
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
        'message': msg,
        'anchor': anchor,
        'last_updated': last_updated
    }
    return render(request, 'index.html', context)


def keepawake(request):
    return HttpResponse(headers={'Status': 'OK'})
