from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post


def home(request: HttpRequest) -> HttpResponse:
    last_posts = Post.objects.select_related("category").order_by("-created_at")[:5]
    return render(request, "home.html", {"last_posts": last_posts})


def post_detail(
    request: HttpRequest, category_slug: str, post_slug: str
) -> HttpResponse:
    post = get_object_or_404(Post, slug=post_slug, category__slug=category_slug)
    return render(request, "post_detail.html", {"post": post})
