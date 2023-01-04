from django.urls import path, re_path

from . import views


app_name = 'blog'

urlpatterns = [
    re_path(r'^signup/$', views.signup, name='signup'),


    path('', views.index, name='index'),
    re_path(r'^add/post/$', views.add_post, name='add_post'),
    re_path(r'^user/posts/$', views.get_user_posts, name='get_user_posts'),
    re_path(r'^user/settings/$', views.settings, name='settings'),
    re_path(r'^user/post/edit/(?P<post_id>[\d]+)', views.edit_post, name='edit_post'),

    re_path(r'^posts/$', views.PostListView.as_view(), name='posts'),
    re_path(r'^posts/draft/$', views.PostDraftListView.as_view(), name='draft_post'),

    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,  name='post_detail'),
    re_path(r'^posts/(?P<teg>[#\w]+)', views.post_list_for_teg, name='post_list_for_teg'),

]
