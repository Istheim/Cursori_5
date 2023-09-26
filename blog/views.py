import random

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Blog
from blog.services import get_posts
from customer.models import Customer
from mailing.models import Sending


class PostListView(ListView):
    model = Blog
    template_name = 'blog/list_blogs.html'


class PostDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail_post.html'

    def get_object(self, queryset=None):
        object = Blog.objects.get(pk=self.kwargs['pk'])
        if object:
            object.count_views += 1
            object.save()
        return object


def index(request):
    context = {
        'posts': get_posts(),
        'title': 'Главная страница',
        'all_sending': Sending.objects.all().count(),
        'sending': Sending.objects.filter(status_sending=Sending.ACTIVATED).count(),
        'unique_customers': Customer.objects.all().count()
    }
    return render(request, 'blog/index.html', context)