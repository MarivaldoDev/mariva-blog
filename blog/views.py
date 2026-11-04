from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post


def home(request: HttpRequest) -> HttpResponse:
    post = get_object_or_404(Post, slug="primeir-post")
    return render(request, "home.html", {"post": post})
