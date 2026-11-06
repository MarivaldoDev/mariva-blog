from typing import ClassVar

from django.contrib import admin
from django.db import models
from martor.widgets import AdminMartorWidget

from .models import Category, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at", "updated_at")
    list_filter = ("category", "created_at", "updated_at")
    formfield_overrides: ClassVar = {
        models.TextField: {"widget": AdminMartorWidget},
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
