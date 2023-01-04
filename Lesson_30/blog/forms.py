from django import forms


from .models import Comment, Teg, Post
from django.contrib.auth.models import User


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class TegForm(forms.ModelForm):

    class Meta:
        model = Teg
        fields = ('teg_name',)


class PostForm(forms.ModelForm):
    slug = forms.SlugField()

    class Meta:
        model = Post
        # fields = ('title', 'slug', 'author', 'body', 'publish', 'status', 'teg',)
        fields = '__all__'


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('last_login', 'is_superuser', 'is_staff', 'date_joined', 'user_permissions', 'groups', 'password')
        # default = {'author_id': 'user.get_id'}
