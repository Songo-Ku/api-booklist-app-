from django.urls import path, include

from . import views

app_name = 'booklist'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book-import/', views.BookImportView.as_view(), name='book-import'),
    path('book-create-manually/', views.BookCreateView.as_view(), name='book-create-manually'),
    path('book/<int:id>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:id>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('booksearchpag/', views.BookListViewSearchView.as_view(), name='booksearchpag'),
]