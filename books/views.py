from .models import Book
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'book_list'
    login_url = 'account_login'
    redirect_field_name = 'next'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    login_url = 'account_login'
    redirect_field_name = 'next'
    permission_required = 'books.special_status'
#    permission_denied_message = 'sorry 2 b u'


class SearchResultsView(ListView):
    model = Book
    template_name = 'books/search_results.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
