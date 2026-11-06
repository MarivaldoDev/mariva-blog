from autoslug import AutoSlugField
from django.db import models
from martor.models import MartorField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        max_length=150,
        always_update=True,
    )  # type: ignore

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(
        populate_from="title",
        unique=True,
        max_length=250,
        always_update=True,
    )  # type: ignore
    content = MartorField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
