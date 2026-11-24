from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from blog.models import Category, Post

from ..forms.category_forms import CategoryForm


@staff_member_required
def list_categories(request):
    categories = (
        Category.objects.annotate(post_count=Count("posts"))
        .prefetch_related("posts")
        .order_by("name")
    )
    return render(request, "dashboard/categories.html", {"categories": categories})


@staff_member_required
def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
    else:
        form = CategoryForm()

    return render(request, "dashboard/create_category.html", {"form": form})


@staff_member_required
@require_http_methods(["POST", "DELETE"])
def delete_category(request, slug: str):
    category = get_object_or_404(Category, slug=slug)
    deleted_posts_count = Post.objects.filter(category=category).count()
    deleted_category_name = category.name
    category.delete()

    if deleted_posts_count:
        messages.success(
            request,
            f'A categoria "{deleted_category_name}" e seus {deleted_posts_count} '
            f"post{'s' if deleted_posts_count != 1 else ''} associados foram excluídos.",
        )
    else:
        messages.success(
            request,
            f'A categoria "{deleted_category_name}" foi excluída.',
        )

    return redirect("dashboard:list_categories")
