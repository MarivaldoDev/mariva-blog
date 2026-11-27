from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Post


def home(request: HttpRequest) -> HttpResponse:
    last_posts = (
        Post.objects.select_related("category")
        .filter(status="published")
        .order_by("-created_at")[:12]
    )
    categories = (
        Category.objects.annotate(
            post_count=Count(
                "posts",
                filter=Q(posts__status=Post.Status.PUBLISHED),
            )
        )
        .filter(post_count__gt=0)
        .order_by("name")
    )

    return render(
        request,
        "home.html",
        {"last_posts": last_posts, "categories": categories},
    )


def post_detail(
    request: HttpRequest, category_slug: str, post_slug: str
) -> HttpResponse:
    post = get_object_or_404(
        Post.objects.select_related("category"),
        slug=post_slug,
        category__slug=category_slug,
    )
    return render(request, "post_detail.html", {"post": post})
