from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView

from booklist.forms import BookModelForm
from booklist.models import Book
from booklist.utils_google_book_api import BooksImporterApi


class IndexView(ListView):
    template_name = 'booklist/index.html'
    context_object_name = 'booklist'
    model = Book

    def get_queryset(self):
        return Book.objects.all().order_by('-id')


class BookImportView(TemplateView):
    template_name = 'booklist/import_phrase.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        phrase = request.POST.get('phrase', '')
        if not phrase:
            message = 'field is empty pls input some phrase'
            return render(request, 'booklist/import_failed.html', {'error_message': message})
        try:
            books_importer = BooksImporterApi(phrase)
            books_importer.run()
        except Exception as message:
            return render(request, 'booklist/import_failed.html', {'error_message': message})
        print(type(books_importer.objects))
        for book_preparation in books_importer.objects:
            books_importer.objects_books.append(
                Book(title=book_preparation['title'],
                     authors_name=book_preparation['authors'],
                     published_date=book_preparation['publishedDate'],
                     isbn13_number=book_preparation['isbn_13'],
                     page_number=book_preparation['pageCount'],
                     language_book=book_preparation['language'],
                     link_book_cover=book_preparation['link_book_cover'],
                     )
            )
        Book.objects.bulk_create(books_importer.objects_books)
        return render(request, 'booklist/import_success.html', {'amount': books_importer.how_many_objects()})


class BookCreateView(CreateView):
    template_name = 'booklist/book_create_form.html'
    form_class = BookModelForm
    queryset = Book.objects.all()
    success_url = reverse_lazy('booklist:index')

    def form_valid(self, form):
        # print('to jest cleaned data \n', form.cleaned_data)
        return super().form_valid(form)


class BookDetailView(DetailView):
    template_name = 'booklist/book_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Book, id=id_)


class BookUpdateView(UpdateView):
    template_name = 'booklist/book_update_form.html'
    form_class = BookModelForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Book, id=id_)

    def get_success_url(self):
        book_id = self.kwargs['id']
        return reverse_lazy('booklist:book_detail', kwargs={'id': book_id})

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class BookListViewSearchView(ListView):
    template_name = 'booklist/book_listview_filter_search.html'
    model = Book
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        print('args: ', args)
        print('kwargs: ', kwargs)
        print('to jest request z get : ', request)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # search: https://learndjango.com/tutorials/django-search-tutorial
        queryset = super().get_queryset()
        # print(queryset)
        print('to jest title z request GET get: ', self.request.GET.get('title', ''))
        search_field = self.request.GET.get('search_field', '')
        print('to jest search field\n', search_field)
        if search_field:
            query = Q()
            query |= Q(title__icontains=search_field)
            query |= Q(authors_name__icontains=search_field)
            query |= Q(language_book__icontains=search_field)
            order_search_map = {
                'ascending_title': 'title',
                'descending_title': '-title',
                'ascending_page_number': 'page_number',
                'descending_page_number': '-page_number',
                'ascending_language_book': 'language_book',
                'descending_language_book': '-language_book',
            }
            queryset = queryset.order_by(order_search_map.get(self.request.GET.get('order_search')))
            return queryset.filter(query)
        query = Q()
        title = self.request.GET.get('title', '')
        if title:
            query &= Q(title__icontains=title)
        published_date_gte = self.request.GET.get('published_date_from', '')
        if published_date_gte:
            query &= Q(published_date__gte=published_date_gte)
        published_date_lte = self.request.GET.get('published_date_to', '')
        if published_date_lte:
            query &= Q(published_date__lte=published_date_lte)
        authors_name = self.request.GET.get('authors_name', '')
        if authors_name:
            query &= Q(authors_name__icontains=authors_name)
        language_book = self.request.GET.get('language_book', '')
        if language_book:
            query &= Q(language_book__icontains=language_book)
        # print('querysecik before filtered field added to filter:   \n', queryset)
        # print('to jest queryset: \n', queryset.filter(query))
        if self.request.GET.get('ordering'):
            order_map = {
                'ascending_title': 'title',
                'descending_title': '-title',
                'ascending_pub_date': 'published_date',
                'descending_pub_date': '-published_date',
                'ascending_page_number': 'page_number',
                'descending_page_number': '-page_number',
                'ascending_language_book': 'language_book',
                'descending_language_book': '-language_book',
            }
            queryset = queryset.order_by(order_map.get(self.request.GET.get('ordering')))
        return queryset.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_dict = {}
        form_dict_order = {}
        # print('czyli to jest context object_list:   ', context['object_list'], '\n i page obj: \n', context['page_obj'])
        form_dict.update(
            language_book=self.request.GET.get('language_book', ''),
            title=self.request.GET.get('title', ''),
            published_date_to=self.request.GET.get('published_date_to', ''),
            published_date_from=self.request.GET.get('published_date_from', ''),
            authors_name=self.request.GET.get('authors_name', ''),
            ordering=self.request.GET.get('ordering', 'descending_pub_date'),
        )
        form_dict_order.update(
            order_search=self.request.GET.get('order_search', 'ascending_title'),
        )
        context['form'] = InputFormFilter(initial=form_dict)
        context['form_search'] = InputFormSearch(initial=form_dict_order)
        if self.request.GET.get('search_field', ''):
            context['search_field_found'] = self.request.GET.get('search_field', '')
        _request_copy = self.request.GET.copy()
        parameters = _request_copy.pop('page', True) and _request_copy.urlencode()
        context['parameters'] = parameters
        return context
