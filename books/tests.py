from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Book, Review
from .views import BookListView, BookDetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class BookTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='reviewuser',
            email='reviewuser@mail.com',
            password='testpass123',
        )
        self.special_permission = Permission.objects.get(
            codename='special_status')
        self.book = Book.objects.create(
            title='Harry Potter',
            author='JK Rowling',
            price='25.00',)
        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='An excellent book!',
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email='reviewuser@mail.com',password='testpass123')
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        self.assertContains(response, 'Harry Potter')

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse('books:book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '%s?next=/books/' % (reverse('account_login')))
        response = self.client.get('%s?next=/books/' % (reverse('account_login')))
        self.assertContains(response, 'Log In')

    def test_book_list_resolves_correct_view(self):
        view = resolve('/books/')
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewuser@mail.com', password='testpass123')
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        self.assertContains(response, 'An excellent book!')

    def test_book_detail_view_without_permissions(self):
        self.client.login(email='reviewuser@mail.com', password='testpass123')
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_book_detail_resolves_correct_view(self):
        view = resolve(f'/books/{self.book.id}/')
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)
