from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from blog.models import Category, Post
from blog.templatetags.markdown_filters import render_markdown

from ..forms.post_forms import PostForm


@staff_member_required
def index(request):
    search_query = request.GET.get("q", "").strip()
    posts = Post.objects.select_related("category").order_by("-created_at")

    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(category__name__icontains=search_query)
        )

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "posts": page_obj.object_list,
        "post_count": Post.objects.count(),
        "category_count": Category.objects.count(),
        "search_query": search_query,
        "displayed_post_count": posts.count(),
        "page_obj": page_obj,
    }

    if request.headers.get("HX-Request"):
        return render(request, "dashboard/_post-results.html", context)

    return render(request, "dashboard/index.html", context)


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
def preview_post(request) -> JsonResponse:
    content = request.POST.get("content", "")
    rendered = render_markdown(content)
    return JsonResponse({"html": rendered})


@staff_member_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f'Post "{post.title}" atualizado com sucesso.')
            return redirect("dashboard:index")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "dashboard/update_post.html",
        {
            "form": form,
            "post": post,
            "post_count": Post.objects.count(),
        },
    )


@staff_member_required
@require_http_methods(["POST", "DELETE"])
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, f'Post "{post.title}" deletado com sucesso.')

    return redirect("dashboard:index")
