from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import request, HttpResponseRedirect
from django.views import generic

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Teg
from .forms import CommentForm, TegForm, PostForm, UserSettingsForm


def index(request):
    return render(request, './index.html')


class PostListView(generic.ListView):
    model = Post
    # queryset = Post.published.all()
    queryset = Post.objects.filter(status='published')
    paginate_by = 3
    template_name = 'blog/post_list.html'


class PostDraftListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status='draft')
    paginate_by = 3
    template_name = 'blog/post_list.html'


def post_detail(request, year, month, day, post):
    """Post detail"""
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        teg_form = TegForm(data=request.POST)
        comment_form = CommentForm(data=request.POST)

        if 'teg_name' in request.POST:
            if teg_form.is_valid():
                new_teg = teg_form.save(commit=False)
                new_teg.save()
                new_teg.post_set.add(post)
                messages.success(request, 'You create new teg and added it to current post',
                                 extra_tags='teg list-group-item list-group-item-success')
            elif post in Teg.objects.get(teg_name=teg_form.data.get('teg_name')).post_set.all():
                messages.warning(request, 'This teg already added.',
                                 extra_tags='teg list-group-item list-group-item-warning')
            else:
                if teg := Teg.objects.get(teg_name=teg_form.data.get('teg_name')):
                    teg.post_set.add(post)
                    messages.success(request, 'You added teg to current post',
                                     extra_tags='teg list-group-item list-group-item-success')

        if 'body' in request.POST:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                messages.success(request, 'You added new comment to current post',
                                 extra_tags='list-group-item list-group-item-success')

        url = request.build_absolute_uri()
        return HttpResponseRedirect(url)

    else:
        comment_form = CommentForm()
        teg_form = TegForm()
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'teg_form': teg_form
    }
    return render(
        request,
        'blog/post_detail.html',
        context)


def post_list_for_teg(request, teg=None):
    """List of published posts with teg."""
    teg = Teg.objects.get(teg_name=teg)
    object_list = teg.post_set.filter(status='published')

    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        'page': posts,
        'post_list': posts,
        'teg': teg,

    }
    return render(
        request,
        'blog/post_list_for_teg.html',
        context
    )


@login_required
def add_post(request):
    post_form = PostForm()

    if request.method == 'POST':
        post_form = PostForm(data=request.POST)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'You added new post',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
        url = request.build_absolute_uri()
        return HttpResponseRedirect(url)

    context = {'post_form': post_form}
    return render(request, 'blog/add_post.html', context)


@login_required
def get_user_posts(request):
    user_posts = Post.objects.filter(author=request.user)
    if not user_posts:
        messages.warning(request, 'You have not created any post yet.',
                         extra_tags='list-group-item list-group-item-success')
        return redirect('blog:add_post')

    context = {'post_list': user_posts}
    return render(request, 'blog/post_list_user.html', context)


@login_required
def edit_post(request, post_id=None):
    post = get_object_or_404(Post, id=post_id)
    post_form = PostForm(instance=post)
    if request.method == 'POST':
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            post.title = post_form.data.get('title')
            # post.slug = post_form.data.get('slug')
            post.user = post_form.data.get('author')
            post.body = post_form.data.get('body')
            post.publish = post_form.data.get('publish')
            post.status = post_form.data.get('status')
            post.post_set = post_form.data.get('teg')
            post.save()

            messages.success(request, 'Post updated.',
                             extra_tags='list-group-item list-group-item-success')
        else:

            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
            context = {'post_form': post_form}
            return render(request, 'blog/add_post.html', context)

        return render(request, 'blog/post_detail.html', {'post': post})

    context = {'post_form': post_form}
    return render(request, 'blog/add_post.html', context)


def signup(request):
    signup_form = UserCreationForm()

    if request.method == 'POST':
        signup_form = UserCreationForm(data=request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            login(request, new_user)
            messages.success(request, 'Welcome to site',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
            url = request.build_absolute_uri()
            return HttpResponseRedirect(url)

        return redirect('blog:index')
    context = {'signup_form': signup_form}
    return render(request, 'registration/signup.html', context)


@login_required
def settings(request):
    user = get_object_or_404(User, pk=request.user.id)
    settings_form = UserSettingsForm(instance=user)

    if request.method == 'POST':
        settings_form = UserSettingsForm(data=request.POST)
        if settings_form.is_valid():
            # user.username = settings_form.data.get('username')
            user.first_name = settings_form.data.get('first_name')
            user.last_name = settings_form.data.get('last_name')
            user.email = settings_form.data.get('email')
            user.save()

            messages.success(request, 'You change your settings.',
                             extra_tags='list-group-item list-group-item-success')
        else:
            messages.error(request, 'something wrong',
                           extra_tags='list-group-item list-group-item-success')
        context = {'settings_form': settings_form}
        return render(request, 'registration/settings.html', context)

    context = {'settings_form': settings_form}
    return render(request, 'registration/settings.html', context)
