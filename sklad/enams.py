from sklad.models import Status


messages = {
    Status.COLLECTED: {
        'subject': 'Заказ собран',
        'message': 'QR-code'
    },
    Status.CANCELED: {
        'subject': 'Заказ отменен',
        'message': 'Нет товара на складе'
    }
}