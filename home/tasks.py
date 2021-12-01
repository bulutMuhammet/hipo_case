import django
from celery.utils.log import get_task_logger

from home.models import Card, Transaction

logger = get_task_logger(__name__)


from core.celery import app

django.setup()
@app.task(name='top_up')
def top_up():
    cards = Card.objects.all()
    for card in cards:
        Transaction.objects.create(transaction_type="top-up", card_id=card.id)
    logger.info("Process ran")

