from sklad.models import Status


messages = {
    Status.COLLECTED: {
        'subject': 'Заказ собран',
        'message': 'Ваш заказ собран!\n'
                   'Отсканируйте qr код, и подтвердите получение заказа! '
    },
    Status.CANCELED: {
        'subject': 'Заказ отменен',
        'message': 'Нет товара на складе'
    }
}

menu = [
    {
        'url_name': 'vendor_list',
        'title': 'Поставщики'
    },
    {
        'url_name': 'buyer_list',
        'title': 'Покупатели'
    },
    {
        'url_name': 'nomenclature_list',
        'title': 'Номеклатура'
    },
    {
        'url_name': 'delivery_list',
        'title': 'Поставка'
    },
    {
        'url_name': 'shipment_list',
        'title': 'Отгрузка'
    },
]