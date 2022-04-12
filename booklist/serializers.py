from rest_framework import serializers

from booklist.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['*']


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title", "language_book", "published_date", "isbn13_number",
                  "page_number", "created", "authors_name", "link_book_cover", "updated"
        ]
