from django.test import TestCase
from django.urls import reverse, resolve
from .models import Book
from .views import BookListView, BookDetailView


class BookTests(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00',)

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, 'Harry Potter')

    def test_book_list_resolves_correct_view(self):
        view = resolve('/books/')
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_detail_resolves_correct_view(self):
        view = resolve(f'/books/{self.book.id}/')
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)
