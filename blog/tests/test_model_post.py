from django.db.utils import DataError

from .test_base import TestBase


class PostModelTest(TestBase):
    def setUp(self):
        self.post = self.make_post()
        return super().setUp()

    def test_post_str_method(self):
        self.assertEqual(str(self.post), self.post.title)

    def test_post_slug_is_generated_on_save(self):
        post = self.make_post(title="My First Post")
        self.assertEqual(post.slug, "my-first-post")

    def test_post_slug_is_not_required_on_creation(self):
        post = self.post
        self.assertIsNotNone(post.slug)

    def test_post_slug_is_unique(self):
        post1 = self.make_post(title="Django", slug="django")
        post2 = self.make_post(title="Django", slug="django-2")
        self.assertNotEqual(post1.slug, post2.slug)

    def test_post_title_cant_length_exceed_200_characters(self):
        with self.assertRaises(DataError):
            self.make_post(title="a" * 201)
