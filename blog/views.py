from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        return Post.objects.filter(author=self.author).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class PostUpdateView(AuthorOnlyMixin, UpdateView):
    model = Post
    fields = ["title", "content"]


class PostDeleteView(AuthorOnlyMixin, DeleteView):
    model = Post
    success_url = "/"


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
