from .models import Status

# Контент для тела письма покупателю.
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
# Список элементов меню раздела Поставка.
delivery_menu = [
    {
        'url_name': 'delivery_add',
        'title': 'Создать заявку',
    }
]

# Список элементов меню раздела Отгрузка.
shipment_menu = [
    {
        'url_name': 'shipment_add',
        'title': 'Создать заявку',
    }
]
