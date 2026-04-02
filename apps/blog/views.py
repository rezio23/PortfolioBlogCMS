from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .filters import PostFilterForm
from .forms import PostForm
from .models import Category, Post, Tag
from .utils import reading_time


POSTS_PER_PAGE = 6


def paginate(request, queryset):
    paginator = Paginator(queryset, POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def blog_list(request):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author", "category").prefetch_related("tags")
    filter_form = PostFilterForm(request.GET or None)
    if filter_form.is_valid():
        queryset = filter_form.filter_queryset(queryset)
    page_obj = paginate(request, queryset)
    context = {"filter_form": filter_form, "page_obj": page_obj, "posts": page_obj.object_list}
    return render(request, "blog/blog_list.html", context)


def blog_detail(request, slug):
    queryset = Post.objects.select_related("author", "category").prefetch_related("tags")
    if request.user.is_authenticated:
        post = get_object_or_404(queryset, slug=slug)
        if post.status != Post.Status.PUBLISHED and post.author != request.user:
            raise PermissionDenied
    else:
        post = get_object_or_404(queryset, slug=slug, status=Post.Status.PUBLISHED)

    return render(
        request,
        "blog/blog_detail.html",
        {"post": post, "reading_time": reading_time(post.content)},
    )


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    queryset = category.posts.filter(status=Post.Status.PUBLISHED)
    page_obj = paginate(request, queryset)
    return render(request, "blog/category_posts.html", {"category": category, "page_obj": page_obj, "posts": page_obj.object_list})


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    queryset = tag.posts.filter(status=Post.Status.PUBLISHED)
    page_obj = paginate(request, queryset)
    return render(request, "blog/tag_posts.html", {"tag": tag, "page_obj": page_obj, "posts": page_obj.object_list})


def search_results(request):
    query = request.GET.get("q", "").strip()
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query)
        )
    page_obj = paginate(request, queryset)
    return render(request, "blog/search_result.html", {"query": query, "page_obj": page_obj, "posts": page_obj.object_list})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, "Post created successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = PostForm()
    return render(request, "blog/post_create.html", {"form": form})


@login_required
def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect(post.get_absolute_url())
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_update.html", {"form": form, "post": post})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied

    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect("blog:my_posts")

    return render(request, "blog/post_delete.html", {"post": post})


@login_required
def my_posts(request):
    queryset = Post.objects.filter(author=request.user)
    page_obj = paginate(request, queryset)
    return render(request, "blog/my_posts.html", {"page_obj": page_obj, "posts": page_obj.object_list})