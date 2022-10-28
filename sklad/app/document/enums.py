from app.document.models import Status

# Контекст для тела письма покупателю.
messages = {
    (Status.VALIDATING, Status.COLLECTED): {
        'subject': 'Заказ собран',
        'message': 'Ваш заказ собран!\n'
                   'Отсканируйте qr код, и подтвердите получение заказа!'
    },
    (Status.VALIDATING, Status.CANCELED): {
        'subject': 'Заказ отменен',
        'message': 'Нет товара на складе'
    },
    (Status.COLLECTED, Status.CANCELED): {
        'subject': 'Заказ отменен',
        'message': 'Истекло время хранения заказа!'
    }
}
