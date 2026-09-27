from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogSmokeTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user("alice", "alice@example.com", "s3cure-pass-123")
        self.bob = User.objects.create_user("bob", "bob@example.com", "s3cure-pass-123")
        self.post = Post.objects.create(title="Hello", content="First post", author=self.alice)

    def test_profile_created_by_signal(self):
        self.assertTrue(hasattr(self.alice, "profile"))

    def test_public_pages_render(self):
        for url in [reverse("blog-home"), reverse("blog-about"), reverse("post-detail", args=[self.post.pk]),
                    reverse("user-posts", args=["alice"]), reverse("register"), reverse("login")]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_create_requires_login(self):
        self.assertEqual(self.client.get(reverse("post-create")).status_code, 302)

    def test_author_can_create_and_edit(self):
        self.client.login(username="alice", password="s3cure-pass-123")
        r = self.client.post(reverse("post-create"), {"title": "New", "content": "Body"})
        self.assertEqual(r.status_code, 302)
        new = Post.objects.get(title="New")
        self.assertEqual(new.author, self.alice)
        r = self.client.post(reverse("post-update", args=[new.pk]), {"title": "Edited", "content": "Body"})
        self.assertEqual(Post.objects.get(pk=new.pk).title, "Edited")

    def test_other_user_cannot_edit_or_delete(self):
        self.client.login(username="bob", password="s3cure-pass-123")
        self.assertEqual(self.client.get(reverse("post-update", args=[self.post.pk])).status_code, 403)
        self.assertEqual(self.client.post(reverse("post-delete", args=[self.post.pk])).status_code, 403)
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_register_flow(self):
        r = self.client.post(reverse("register"), {"username": "carol", "email": "c@example.com",
                                                    "password1": "An0ther-strong-pass", "password2": "An0ther-strong-pass"})
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username="carol").exists())
