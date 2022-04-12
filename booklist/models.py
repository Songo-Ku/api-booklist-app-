from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    language_book = models.CharField(max_length=40)
    published_date = models.DateField(help_text="example: 2017-03-14")
    isbn13_number = models.CharField(max_length=15)
    page_number = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    authors_name = models.CharField(max_length=300)
    link_book_cover = models.URLField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} {self.published_date}'




