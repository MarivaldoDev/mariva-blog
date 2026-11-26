from django.test import TestCase

from ..models import Category, Post


class TestBase(TestCase):
    def make_category(self, name: str = "Django", slug: str | None = None) -> Category:
        return Category.objects.create(name=name, slug=slug)

    def make_post(
        self,
        title: str = "Primeiro Post",
        content: str = "Conteúdo do primeiro post",
        slug: str | None = None,
        category: Category | None = None,
        image: str | None = None,
        status: Post.Status = Post.Status.DRAFT,
    ) -> Post:

        if category is None:
            category = self.make_category()
        return Post.objects.create(
            title=title,
            content=content,
            category=category,
            slug=slug,
            image=image,
            status=status,
        )
