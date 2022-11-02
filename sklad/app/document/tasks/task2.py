from datetime import datetime

from config.settings import DOCUMENT_TIME_OUT
from config.celery import app
from app.document.models import Document, Status

from app.document.services import ChangeDocumentStatus


@app.task
def check_document_status():
    day_since = datetime.now() - DOCUMENT_TIME_OUT
    documents = Document.objects.filter(time_update__lte=day_since).filter(
        status=Status.COLLECTED
    )
    for document in documents:
        ChangeDocumentStatus.execute(document, Status.CANCELED)
