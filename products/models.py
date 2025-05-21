from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from core.models import TimestampModel
from colorfield.fields import ColorField

from taggit.managers import TaggableManager
from core.utils.common import ninja_reverse
from django.core.validators import MinValueValidator, MaxValueValidator


# class Comment(models.Model):
#     user = None
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments')
#     body = models.TextField()
#
#
# class Reply(models.Model):
#     user = None
#     comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies')
#     body = models.TextField()


class Category(TimestampModel):
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='children', on_delete=models.CASCADE
    )
    title = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True, allow_unicode=True)
    thumbnail = models.ImageField(upload_to='categories', null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title, allow_unicode=True)

        # prevent a category to be itself parent
        if self.id and self.parent and self.id == self.parent.id:
            self.parent = None

        return super().save(*args, **kwargs)

    @property
    def detail_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return ninja_reverse("categories@detail", args=[self.slug])

    @property
    def thumbnail_url(self):
        try:
            return self.thumbnail.url
        except:
            return None


class Product(TimestampModel):
    title = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), allow_unicode=True)
    price = models.PositiveIntegerField(_('price'))
    discount_price = models.PositiveIntegerField(_('discounted price'))  # TODO: Filter with this discount price not the price
    discount_percentage = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    is_discount = models.BooleanField(_('is discount'))

    thumbnail = models.ImageField(upload_to='products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('category'))

    tags = TaggableManager(verbose_name=_('tags'))
    description = models.TextField(_('Description'))
    colors = models.ManyToManyField('ProductColor', related_name='products')

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title, allow_unicode=True)
        self.is_discount = bool(self.discount_percentage)
        if self.discount_percentage is None:
            self.discount_percentage = 0

        if self.discount_percentage == 0:
            self.discount_price = self.price
        else:
            self.discount_price = self.price - ((self.price * self.discount_percentage) / 100)

        return super().save(*args, **kwargs)

    @property
    def detail_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return ninja_reverse("products@detail", args=[self.id])

    @property
    def thumbnail_url(self):
        try:
            return self.thumbnail.url
        except:
            return None


class ProductColor(models.Model):
    color = ColorField(verbose_name=_('color'))
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('Description'), null=True, blank=True)

    def __str__(self):
        return self.name
