from django.db.utils import DataError

from .test_base import TestBase


class CategoryModelTest(TestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()

    def test_cateory_str_method(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_category_slug_is_generated_on_save(self):
        category = self.make_category(name="Deploy")
        self.assertEqual(category.slug, "deploy")

    def test_category_slug_is_not_required_on_creation(self):
        category = self.category
        self.assertIsNotNone(category.slug)

    def test_category_slug_is_unique(self):
        category1 = self.make_category(name="Flask", slug="flask")
        category2 = self.make_category(name="Flask", slug="flask-2")
        self.assertNotEqual(category1.slug, category2.slug)

    def test_category_name_cant_lenght_exceed_100_characters(self):
        with self.assertRaises(DataError):
            self.make_category(name="a" * 101)
