from django.urls import path

from .views import (
    blog_detail,
    blog_list,
    category_posts,
    my_posts,
    post_create,
    post_delete,
    post_update,
    search_results,
    tag_posts,
)

app_name = "blog"

urlpatterns = [
    path("", blog_list, name="blog_list"),
    path("search/", search_results, name="search_result"),
    path("category/<slug:slug>/", category_posts, name="category_posts"),
    path("tag/<slug:slug>/", tag_posts, name="tag_posts"),
    path("create/", post_create, name="post_create"),
    path("my-posts/", my_posts, name="my_posts"),
    path("<slug:slug>/edit/", post_update, name="post_update"),
    path("<slug:slug>/delete/", post_delete, name="post_delete"),
    path("<slug:slug>/", blog_detail, name="blog_detail"),
]
