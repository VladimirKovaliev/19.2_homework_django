from django.db import models

from blog.models import NULLABLE


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}, {self.description}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='products/', verbose_name='превью', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='цена за штуку')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='автор', **NULLABLE,)
    publication = models.BooleanField(default=False, verbose_name='публикация')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            (
                'set_published',
                'Can publish posts'
            )
        ]
    def __str__(self):
        return f'{self.name}, {self.description}, {self.price}'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(verbose_name='Номер версии')
    version_name = models.CharField(max_length=50, verbose_name='Название версии', unique=True)
    activate = models.BooleanField(default=False, verbose_name='Признак')

    def __str(self):
        return f'{self.version_name} ({self.version_number})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'