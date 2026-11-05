from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:slug>/<slug:post_slug>/", views.post_detail, name="post_detail"),
]
