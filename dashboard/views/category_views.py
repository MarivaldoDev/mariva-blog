from django.shortcuts import redirect, render

from ..forms import CategoryForm


def create_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard:index")
    else:
        form = CategoryForm()

    return render(request, "dashboard/create_category.html", {"form": form})
