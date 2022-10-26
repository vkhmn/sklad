from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    """ Категория номенклатуры """

    name = models.CharField('Категория', max_length=100, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    """ Подкатегория номенклатуры """

    name = models.CharField('Подкатегория', max_length=100, unique=True)
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


class Store(models.Model):
    """ Остаток на складе """

    nomenclature = models.OneToOneField(
        Nomenclature,
        on_delete=models.CASCADE,
        verbose_name='Номенклатура'
    )
    amount = models.IntegerField(
        'Количество',
        default=0
    )

    def __str__(self):
        return f'{self.nomenclature} - {self.amount}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


@receiver(post_save, sender=Nomenclature)
def update_stock(sender, instance, **kwargs):
    Store.objects.create(nomenclature=instance)
