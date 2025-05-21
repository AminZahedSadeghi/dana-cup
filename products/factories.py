import random

import factory
from django.conf import settings
from factory.django import DjangoModelFactory
from taggit.models import Tag

from .models import Product, Category, ProductColor


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.Sequence(lambda n: f'تگ{n}')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f'کتگوری{n}')


def random_discount_percentage():
    has_discount = random.choice([True, False])
    if has_discount:
        return random.randrange(5, 95, step=5)
    return 0


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    title = factory.Faker('name')
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker('sentence', nb_words=37)
    price = factory.Faker('random_int', min=1_000, max=300_000, step=10_000)
    discount_percentage = factory.LazyFunction(random_discount_percentage)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        words = []
        for _ in range(random.randint(2, 7)):
            words.append(settings.FAKE.word())

        self.tags.add(*words)

    @factory.post_generation
    def colors(self, create, extracted, **kwargs):
        if not create:
            return

        product_colors = random.sample(list(ProductColor.objects.all()), k=random.randint(1, 4))
        self.colors.add(*product_colors)
