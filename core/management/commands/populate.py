import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from products.factories import ProductFactory
from products.models import Category, ProductColor

TQDM_COLOURS = ['RED', 'YELLOW', 'BLUE', 'MAGENTA', 'CYAN', 'WHITE']
fake = settings.FAKE

NUM_PRODUCTS = 20
NUM_CATEGORIES = 4
NUM_COLORS = 4


def get_tqdm_color():
    return str(random.choice(TQDM_COLOURS))


class Command(BaseCommand):
    help = "Create fake data for blue ice burner app."

    def __init__(self):
        super().__init__()

    @transaction.atomic
    def handle(self, *args, **options):
        # Categories data
        all_categories = []
        for category_name in tqdm(["آرایش بهداشتی", "کالای دیجیتال", "لوازم خانگی", 'پوشاک'], colour=get_tqdm_color(),
                                  desc=f'Adding {NUM_CATEGORIES} categories'):
            all_categories.append(Category.objects.create(title=category_name))

        all_colors = []
        colors = {
            'قرمز': '#e31818',
            'آبی': '#120bed',
            'سفید': '#FFFFFF',
            'زرد': '#e1f504',
        }
        for color_name, color_code in colors.items():
            all_colors.append(ProductColor.objects.create(name=color_name, color=color_code))

        # Products data
        all_products = []
        for _ in tqdm(range(NUM_PRODUCTS), colour=get_tqdm_color(), desc=f'Adding {NUM_PRODUCTS} products'):
            category = random.choice(all_categories)
            all_products.append(ProductFactory(category=category))
