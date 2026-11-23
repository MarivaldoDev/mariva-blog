from django.urls import path

from .views import category_views, post_views

app_name = "dashboard"

urlpatterns = [
    path("", post_views.index, name="index"),
    path("categories/", category_views.list_categories, name="list_categories"),
    path("category/create/", category_views.create_category, name="create_category"),
    path(
        "category/delete/<slug:slug>/",
        category_views.delete_category,
        name="delete_category",
    ),
    path("post/create/", post_views.create_post, name="create_post"),
    path("post/update/<slug:slug>/", post_views.update_post, name="update_post"),
    path("post/delete/<slug:slug>/", post_views.delete_post, name="delete_post"),
    path("post/preview/", post_views.preview_post, name="preview_post"),
]
