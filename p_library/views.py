from django.db.models import Avg, Count, Q
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from p_library.models import Book, Author
from p_library.models import Publisher


def books_list(request):
    books = Book.objects.all().filter(year_release__gt=1000)
    return HttpResponse(books)


def index(request):
    template = loader.get_template('index.html')
    books = Book.objects.all().annotate(book_authors=Count('author__id'))  #аннотруем количество авторов для каждой книги
    filter1 = Q(country='RU') & Q(birth_year__gt=1500)
    authors = Author.objects.all().annotate(authors_of_book=Count('authors_name__id', filter1)) #аннотруем количество книг, котрые нписал каждый автор
    b = books.aggregate(average_price=Avg('price')) #с помощью агрегации рассчитываем среднюю стоимость ВСЕХ книг
    test_result = Book.objects.filter(title__icontains="ла").first()
    biblio_data = {
        "title": "мою библиотеку",
        "books": books,
        "test_result": test_result,
        "authors": authors,
        "average_price": b['average_price'],
    }
    print(filter1)
    print(list(books.values('author__full_name')))
    return HttpResponse(template.render(biblio_data, request))


def book_increment(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            book.copy_count += 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_decrement(request):
    if request.method == 'POST':
        book_id = request.POST['id']
        if not book_id:
            return redirect('/index/')
        else:
            book = Book.objects.filter(id=book_id).first()
            if not book:
                return redirect('/index/')
            if book.copy_count < 1:
                book.copy_count = 0
            else:
                book.copy_count -= 1
            book.save()
        return redirect('/index/')
    else:
        return redirect('/index/')


def book_publisher(request):
    template = loader.get_template('publisher.html')

    biblio_data = {
        'publishers': Publisher.objects.all()
    }
    return HttpResponse(template.render(biblio_data, request))
