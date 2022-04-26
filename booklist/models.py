from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors_name = models.CharField(max_length=300)
    published_date = models.DateField(help_text="example: 2017-03-14")
    isbn13_number = models.CharField(max_length=15)
    page_number = models.IntegerField(blank=True, null=True)
    link_book_cover = models.URLField(null=True, blank=True)
    language_book = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.title} {self.published_date}'




