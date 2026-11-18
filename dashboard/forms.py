from typing import ClassVar

from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields: ClassVar[list[str]] = ["title", "content", "category"]

        widgets: ClassVar[dict[str, forms.Widget]] = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        title = cleaned_data.get("title")
        if title:
            if Post.objects.filter(title=title).exists():
                raise forms.ValidationError("A post with this title already exists.")

        return cleaned_data
