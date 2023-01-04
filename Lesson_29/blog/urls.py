from django.urls import path, re_path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^posts/$', views.PostListView.as_view(), name='posts'),
    re_path(r'^post/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[-\w]+)$',
            views.PostDetailView.as_view(),
            name='post-detail'),
]
