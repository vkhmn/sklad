from .models import Status


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

delivery_menu = [
    {
        'url_name': 'delivery_add',
        'title': 'Создать заявку',
    }
]
shipment_menu = [
    {
        'url_name': 'shipment_add',
        'title': 'Создать заявку',
    }
]
