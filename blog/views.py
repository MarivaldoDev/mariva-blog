from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post


def home(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", {"posts": posts})


def post_detail(request: HttpRequest, slug: str, post_slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=post_slug, category__slug=slug)
    return render(request, "post_detail.html", {"post": post})
