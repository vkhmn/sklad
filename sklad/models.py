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
    article = models.IntegerField('Артукул', unique=True)
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

    nomenclature = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        verbose_name='Номенклатура'
    )
    amount = models.IntegerField('Количество')

    def __str__(self):
        return f'{self.nomenclature} - {self.amount}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'


class Contactor(models.Model):
    """ Контрагент """

    fio = models.CharField('Фамилия Имя Отчество', max_length=100)
    email = models.EmailField('Email')
    phone = models.IntegerField('Телефон')


class Buyer(Contactor):
    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class BankDetails(models.Model):
    """ Банковские реквизиты """

    account = models.IntegerField('Номер счета')
    bank_name = models.CharField('Наименование банка', max_length=100)

    def __str__(self):
        return self.bank_name


class Vendor(Contactor):
    """ Поставщик """

    name = models.CharField('Наименование', max_length=100)
    address = models.CharField('Адрес', max_length=100)
    category = models.ManyToManyField(
        Category,
        verbose_name='Категории'
    )
    bank_details = models.ForeignKey(
        BankDetails,
        on_delete=models.CASCADE,
        verbose_name='Банковские реквизиты'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Status(models.TextChoices):
    """ Статус заявки - choices """

    VALIDATING = 'va', 'Проверка'
    CANCELED = 'ca', 'Отменен'
    COLLECTED = 'co', 'Собран'
    FINISHED = 'fi', 'Завершен'


class Document(models.Model):
    """ Заявка на поставку/отгрузку товаров """

    number = models.IntegerField('Номер заявки')
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Поставщик'
    )
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        default=None,
        verbose_name='Покупатель'
    )
    nomenclatures = models.ManyToManyField(
        Nomenclature,
        through='DocumentNomenclatures',
        verbose_name='Номенклатура'
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.VALIDATING,
        verbose_name='Статус'
    )
    time_create = models.DateTimeField('Время создания', auto_now_add=True)
    time_update = models.DateTimeField('Время обновления статуса', auto_now=True)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class DocumentNomenclatures(models.Model):
    """ Хранит номенклатуру и кол-во в документе """

    nomenclature = models.ForeignKey(
        Nomenclature,
        on_delete=models.CASCADE,
        verbose_name='Номенклатура'
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name='Заявка'
    )
    amount = models.IntegerField('Количество')
