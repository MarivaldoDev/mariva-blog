from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from blog.models import Category

from ..forms.category_forms import CategoryForm


@staff_member_required
def list_categories(request):
    categories = Category.objects.all()
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
    category.delete()

    messages.success(request, f'Category "{category.name}" deletada com sucesso.')

    return redirect("dashboard:index")
