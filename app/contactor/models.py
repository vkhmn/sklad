from django.db import models
from django.urls import reverse

from app.nomenclature.models import Category


class Contactor(models.Model):
    """ Контрагент """

    fio = models.CharField('Фамилия Имя Отчество', max_length=100)
    email = models.EmailField('Email')
    phone = models.IntegerField('Телефон')


class Buyer(Contactor):
    """ Покупатель """

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def get_absolute_url(self):
        return reverse('buyer', kwargs={'pk': self.pk})


class BankDetails(models.Model):
    """ Банковские реквизиты """

    account = models.IntegerField('Номер счета')
    bank_name = models.CharField('Наименование банка', max_length=100)

    def __str__(self):
        return f'{self.bank_name} {self.account}'


class Vendor(Contactor):
    """ Поставщик """

    name = models.CharField('Наименование', max_length=100)
    address = models.CharField('Адрес', max_length=100)
    categories = models.ManyToManyField(
        Category,
        verbose_name='Категории'
    )
    bank_details = models.OneToOneField(
        BankDetails,
        on_delete=models.DO_NOTHING,
        verbose_name='Банковские реквизиты'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('vendor', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

