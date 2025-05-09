import time

from celery import shared_task
# app = Celery()
import logging
logger = logging.getLogger(__name__)

@shared_task()
def celery_test_fun(a, b):
    logger.info("celery task start")
    time.sleep(10)
    logger.info("celery task end")
    return a + b