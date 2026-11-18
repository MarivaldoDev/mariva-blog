from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/create/", views.create_post, name="create_post"),
    path("post/preview/", views.preview_post, name="preview_post"),
]
