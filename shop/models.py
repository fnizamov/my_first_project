from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from slugify import slugify
from .utils import get_time

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, primary_key=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    user = models.ForeignKey(
        verbose_name='Продавец',
        to=User,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/$d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.ManyToManyField(
        to='Tag',
        related_name='products',
        blank=True
    )
           

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)
        index_together = (('id', 'slug'))

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class ProductImage(models.Model):
    image = models.ImageField(upload_to='product_images/carousel')
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_images'
    )


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, primary_key=True)
    slug = models.SlugField(max_length=35, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Comment from {self.user.username} to {self.product.name}'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RAITING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RAITING_CHOICES,
        blank=True,
        null=True)
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    class Meta:
        verbose_name = 'Рейтинг'

    def __str__(self):
        return str(self.rating)