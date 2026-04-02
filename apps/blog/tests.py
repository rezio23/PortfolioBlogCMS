from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Post


class BlogViewsTests(TestCase):
    def test_blog_list_returns_success(self):
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_post_absolute_url(self):
        user = User.objects.create_user(username="author", password="pass12345")
        post = Post.objects.create(author=user, title="Test Post", content="Hello world")
        self.assertEqual(post.get_absolute_url(), reverse("blog:blog_detail", kwargs={"slug": post.slug}))
