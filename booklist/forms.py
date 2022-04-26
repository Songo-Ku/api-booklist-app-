from django import forms
from .models import Book


class DateInput(forms.DateInput):
    input_type = 'date'


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            'title', 'language_book', 'published_date',
            'authors_name', 'isbn13_number', 'page_number', 'link_book_cover'
        )
        widgets = {
            'published_date': DateInput(),
        }


class InputFormFilter(forms.Form):
    published_date_from = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
        required=False,
        label='Daty od ',
    )
    published_date_to = forms.CharField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
        required=False,
        label='Daty do ',
    )
    title = forms.CharField(required=False,)
    language_book = forms.CharField(required=False,)
    authors_name = forms.CharField(required=False,)

    CHOICES = (
        ('ascending_title', 'sortowanie alfabetycznie po tytule'),
        ('descending_title', 'sortowanie nie alfabetycznie po tytule'),
        ('ascending_pub_date', 'rosnąco po datach publikacji'),
        ('descending_pub_date', 'malejąco po datach publikacji'),
        ('ascending_language_book', 'sortowanie alfabetycznie po jezyku ksiazki'),
        ('descending_language_book', 'sortowanie nie alfabetycznie po jezyku ksiazki'),
        ('ascending_page_number', 'sortowanie alfabetycznie po liczbie stron'),
        ('descending_page_number', 'sortowanie nie alfabetycznie po liczbie stron'),
    )
    ordering = forms.CharField(
        widget=forms.Select(choices=CHOICES),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('to sa fields w init: ')
        print(self.fields)


class InputFormSearch(forms.Form):
    search_field = forms.CharField(required=False,)
    CHOICES = (
        ('ascending_title', 'sortowanie alfabetycznie po tytule'),
        ('descending_title', 'sortowanie nie alfabetycznie po tytule'),
        ('ascending_language_book', 'sortowanie alfabetycznie po jezyku ksiazki'),
        ('descending_language_book', 'sortowanie nie alfabetycznie po jezyku ksiazki'),
        ('ascending_page_number', 'sortowanie alfabetycznie po liczbie stron'),
        ('descending_page_number', 'sortowanie nie alfabetycznie po liczbie stron'),
    )
    order_search = forms.CharField(
        widget=forms.Select(choices=CHOICES),
        required=False,
    )













































# -------------------------------------------------------------------------

# good example https://www.fullstackpython.com/django-forms-modelform-examples.html
# from django.forms import ModelForm
# from gears.widgets import DropdownSelectSubmit
# from proceedings.models import CameraReady
# EMPTY_VOLUME_LABEL = '(no volume)'
# class UpdateVolumeForm(ModelForm):
#
#     class Meta:
#         model = CameraReady
#         fields = ['volume']
    # widgets = {
    #     'volume': DropdownSelectSubmit(
    #         empty_label=EMPTY_VOLUME_LABEL,
    #         label_class='font-weight-normal dccn-text-small',
    #         empty_label_class='text-warning-18',
    #         nonempty_label_class='text-success-18',
    #     )
    # }
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['volume'].queryset = self.instance.proc_type.volumes.all()
    #     self.fields['volume'].empty_label = EMPTY_VOLUME_LABEL

    # fields = ['ordering']
    # widgets = {'ordering': Select(choices=CHOICES)}
    # from django.forms import ModelForm, Textarea
    # widgets = {'name': Textarea(attrs={'cols': 80, 'rows': 20}),}
    # verbose_name = "E-Mail Address"  - we can use it as parameter in field

    # widgets = {'published_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})}
    # labels = {
    #     'name': _('Writer'),
    # }
    # help_texts = {
    #     'name': _('Some useful help text.'),
    # }
    # , null = True, blank = True


    # published_date_gte = forms.CharField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # published_date_gte = forms.DateField(widget=forms.widgets.DateInput(format='%Y/%m/%d', attrs={'type': 'date'}))
    # DateField has optional argument  input_formats
    # default = '', blank = True

# DATE_INPUT_FORMATS = ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d')
# class MyModelForm(forms.ModelForm):
#     issue_date = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)












