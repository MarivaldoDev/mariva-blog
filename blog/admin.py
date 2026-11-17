from typing import ClassVar

from django import forms
from django.contrib import admin

from .models import Category, Post


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "markdown-source",
                "rows": 30,
            }
        )
    )

    class Meta:
        model = Post
        fields: ClassVar[list[str]] = ["title", "content", "category"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ("title", "category", "created_at", "updated_at")
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("title", "content")

    class Media:
        js: ClassVar[list[str]] = [
            "blog/dist/markdown-editor.js",
        ]

        css: ClassVar[dict[str, list[str]]] = {
            "all": [
                "blog/dist/markdown-editor.css",
            ]
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
