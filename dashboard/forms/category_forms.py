from typing import ClassVar

from django import forms

from blog.models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields: ClassVar[list[str]] = ["name"]

        widgets: ClassVar[dict[str, forms.Widget]] = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        name = cleaned_data.get("name")
        if name:
            if Category.objects.filter(name=name).exists():
                raise forms.ValidationError("A category with this name already exists.")

        return cleaned_data
