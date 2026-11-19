from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from blog.models import Category, Post
from blog.templatetags.markdown_filters import render_markdown

from ..forms import PostForm


@staff_member_required
def index(request):
    posts = Post.objects.select_related("category").order_by("-created_at")
    return render(
        request,
        "dashboard/index.html",
        {
            "posts": posts[:8],
            "post_count": posts.count(),
            "category_count": Category.objects.count(),
        },
    )


@staff_member_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, f'Post "{post.title}" criado com sucesso.')
            return redirect("dashboard:create_post")
    else:
        form = PostForm()

    return render(
        request,
        "dashboard/create_post.html",
        {
            "form": form,
            "post_count": Post.objects.count(),
        },
    )


@staff_member_required
@require_POST
def preview_post(request):
    content = request.POST.get("content", "")
    rendered = render_markdown(content)
    return JsonResponse({"html": rendered})
