from rest_framework import viewsets, permissions, status

from booklist.models import Book
from booklist.serializers import BookSerializer, BookCreateSerializer


class ContactUserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return
        return super().get_serializer_class()