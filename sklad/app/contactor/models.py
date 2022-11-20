from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse

from app.nomenclature.models import Category


class Person(models.Model):
    """ Контактное лицо """

    full_name = models.CharField('Фамилия Имя Отчество', max_length=100)
    email = models.EmailField('Email', unique=True)
    phone = models.BigIntegerField('Телефон', unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Контактное лицо'
        verbose_name_plural = 'Контактные лица'


class Buyer(models.Model):
    """ Покупатель """
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )

    def __str__(self):
        return self.person.full_name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def get_absolute_url(self):
        return reverse('buyer', kwargs={'pk': self.pk})


class BankDetails(models.Model):
    """ Банковские реквизиты """

    account = models.CharField('Номер счета', max_length=20, unique=True)
    bank_name = models.CharField('Наименование банка', max_length=100)

    def __str__(self):
        return f'{self.bank_name} {self.account}'

    class Meta:
        verbose_name = 'Банковские реквизиты'
        verbose_name_plural = 'Банковские реквизиты'


class Vendor(models.Model):
    """ Поставщик """

    name = models.CharField('Наименование', max_length=100)
    address = models.CharField('Адрес', max_length=100)
    contact_person = models.OneToOneField(
        Person,
        on_delete=models.DO_NOTHING,
        verbose_name='Контактное лицо'
    )
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


@receiver(post_delete, sender=Vendor)
def post_delete_vendor(sender, instance, *args, **kwargs):
    if instance.contact_person:
        instance.contact_person.delete()
    if instance.bank_details:
        instance.bank_details.delete()


@receiver(post_delete, sender=Buyer)
def post_delete_buyer(sender, instance, *args, **kwargs):
    if instance.person:
        instance.person.delete()
