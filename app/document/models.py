from django.db import models
from django.urls import reverse

from app.contactor.models import Vendor, Buyer
from app.nomenclature.models import Nomenclature


class Status(models.TextChoices):
    """ Статус заявки - choices """

    VALIDATING = 'va', 'Проверка'
    CANCELED = 'ca', 'Отменен'
    COLLECTED = 'co', 'Собран'
    FINISHED = 'fi', 'Завершен'


class Document(models.Model):
    """ Заявка на поставку/отгрузку товаров """

    # number = models.IntegerField('Номер заявки')
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name='Поставщик'
    )
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
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

    def get_absolute_url(self):
        return reverse('document', kwargs={'pk': self.pk})

    def __str__(self):
        document_type = 'Поставка' if self.vendor else 'Отгрузка'
        if not (self.buyer or self.vendor):
            document_type = 'None'

        return f'{document_type} № {self.pk}'


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
    amount = models.IntegerField('Количество', default=1)

    def __str__(self):
        return f'{self.nomenclature}  - ({self.amount} шт.)'

    class Meta:
        verbose_name = 'Номенклатура документа'
        verbose_name_plural = 'Номенклатура документа'
