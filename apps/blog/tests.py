from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Post, Tag


class BlogViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="author", password="pass12345")
        self.product_design = Category.objects.create(name="Product Design")
        self.development = Category.objects.create(name="Development")
        self.portfolio = Tag.objects.create(name="portfolio")
        self.django = Tag.objects.create(name="django")

        self.product_post = Post.objects.create(
            author=self.user,
            title="Portfolio Systems for Designers",
            content="Building a portfolio with structure and clarity.",
            excerpt="A design-led post.",
            category=self.product_design,
            status=Post.Status.PUBLISHED,
        )
        self.product_post.tags.add(self.portfolio)

        self.dev_post = Post.objects.create(
            author=self.user,
            title="Django Filtering Notes",
            content="A practical walkthrough of filtering blog content.",
            excerpt="A Django-focused post.",
            category=self.development,
            status=Post.Status.PUBLISHED,
        )
        self.dev_post.tags.add(self.django)

    def test_blog_list_returns_success(self):
        response = self.client.get(reverse("blog:blog_list"))
        self.assertEqual(response.status_code, 200)

    def test_post_absolute_url(self):
        post = Post.objects.create(author=self.user, title="Test Post", content="Hello world")
        self.assertEqual(post.get_absolute_url(), reverse("blog:blog_detail", kwargs={"slug": post.slug}))

    def test_blog_list_filters_by_title(self):
        response = self.client.get(reverse("blog:blog_list"), {"title": "Django"})

        self.assertContains(response, "Django Filtering Notes")
        self.assertNotContains(response, "Portfolio Systems for Designers")

    def test_blog_list_filters_by_category(self):
        response = self.client.get(reverse("blog:blog_list"), {"category": self.product_design.pk})

        self.assertContains(response, "Portfolio Systems for Designers")
        self.assertNotContains(response, "Django Filtering Notes")

    def test_blog_list_filters_by_tag(self):
        response = self.client.get(reverse("blog:blog_list"), {"tag": self.django.pk})

        self.assertContains(response, "Django Filtering Notes")
        self.assertNotContains(response, "Portfolio Systems for Designers")
