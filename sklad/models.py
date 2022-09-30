from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория номенклатуры"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


class SubCategory(models.Model):
    """Подкатегория номенклатуры"""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'pk': self.pk})


class Nomenclature(models.Model):
    """Номенклатура"""
    name = models.CharField(max_length=100)
    article = models.IntegerField(unique=True)
    amount = models.IntegerField()
    price = models.IntegerField()
    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nomenclature', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'


class Buyer(models.Model):
    """Покупатель"""
    fio = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Vendor(models.Model):
    """Поставщик"""
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    fio = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Status(models.TextChoices):
    """Статус заявки - choices"""
    VALIDATING = 'vl', 'На проверке'
    FINISHED = 'fi', 'Завершен'
    CANCELED = 'ca', 'Отменен'


class Delivery(models.Model):
    """Заявка на поставку товаров поставщиком"""
    number = models.IntegerField()
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE
    )
    content = models.ManyToManyField(
        Nomenclature,
        through='DeliveryContent'
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.VALIDATING
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'


class DeliveryContent(models.Model):
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Shipment(models.Model):
    """Заявка на отгрузку товаров покупателю"""
    number = models.IntegerField()
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE
    )
    content = models.ManyToManyField(
        Nomenclature,
        through="ShipmentContent"
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.VALIDATING
    )
    date = models.DateTimeField(auto_now_add=True)
    qr = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('shipment', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Отгрузка'
        verbose_name_plural = 'Отгрузки'


class ShipmentContent(models.Model):
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)
