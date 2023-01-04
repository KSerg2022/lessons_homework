from django.shortcuts import render
from django.views import generic


from .models import Post


def index(request):
    return render(request, './index.html')


class PostListView(generic.ListView):
    model = Post

    queryset = Post.published.all()  # отбор опубликованных постов через класс.
    # queryset = Post.objects.filter(status='published')  # та тоже отбираются только опубликованные посты.

    paginate_by = 2


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
