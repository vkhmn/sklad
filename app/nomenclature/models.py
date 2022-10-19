from django.db import models
from django.urls import reverse


class Category(models.Model):
    """ Категория номенклатуры """

    name = models.CharField('Категория', max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    """ Подкатегория номенклатуры """

    name = models.CharField('Подкатегория', max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Nomenclature(models.Model):
    """ Номенклатура """

    name = models.CharField('Наименование', max_length=100)
    article = models.IntegerField('Артикул', unique=True)
    price = models.IntegerField('Цена')
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nomenclature', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'
