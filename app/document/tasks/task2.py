from datetime import datetime, timedelta

from config.celery import app
from app.document.models import Document, Status

from app.document.services import ChangeDocumentStatus


@app.task
def check_document_status():
    day_since = datetime.now() - timedelta(minutes=2)
    documents = Document.objects.filter(time_update__lte=day_since).filter(
        status=Status.COLLECTED
    )
    for document in documents:
        ChangeDocumentStatus.execute(document, Status.CANCELED)

    print('Check_document_status')
    return day_since.strftime('%d/%m/%y %H - %M - %S')
