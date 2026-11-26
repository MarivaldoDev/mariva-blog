from typing import ClassVar

from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields: ClassVar[list[str]] = [
            "image",
            "title",
            "content",
            "category",
            "status",
        ]
        labels: ClassVar[dict[str, str]] = {
            "image": "Imagem",
            "title": "Título",
            "content": "Conteúdo",
            "category": "Categoria",
            "status": "Status",
        }

        widgets: ClassVar[dict[str, forms.Widget]] = {
            "image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Digite o título do post",
                }
            ),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 18}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        status_field = self.fields["status"]
        if not isinstance(status_field, forms.ChoiceField):
            raise TypeError("O campo status precisa ser um ChoiceField.")
        status_field.choices = [
            (Post.Status.DRAFT, "Rascunho"),
            (Post.Status.PUBLISHED, "Publicado"),
        ]

    def clean(self) -> dict[str, str]:
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        title = cleaned_data.get("title")
        if title:
            duplicate_titles = Post.objects.filter(title=title)
            if self.instance.pk:
                duplicate_titles = duplicate_titles.exclude(pk=self.instance.pk)
            if duplicate_titles.exists():
                raise forms.ValidationError("A post with this title already exists.")

        return cleaned_data
