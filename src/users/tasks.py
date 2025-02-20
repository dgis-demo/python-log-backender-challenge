import structlog
from celery import shared_task
from django.db import transaction
from sentry_sdk import capture_message

from core.event_log_client import EventLogClient
from users.models import EventOutbox

logger = structlog.get_logger(__name__)

@shared_task
def send_outbox_events(batch_size: int) -> None:
    with transaction.atomic():
        events = list(EventOutbox.objects.order_by('id')[:batch_size])

        if not events:
            return

        event_ids = [event.id for event in events]

        try:
            with EventLogClient.init() as client:
                client.insert(data=events)

            EventOutbox.objects.filter(id__in=event_ids).delete()
            logger.info('Successfully processed batch', batch_size=len(events))
        except Exception as e:
            message = 'Failed to process batch'
            capture_message(f'{message}: {e.__class__.__name__}: {e}')
            logger.error(message, error=str(e))
            raise
