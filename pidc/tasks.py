import os
import time

from celery import Celery

from .gennifer_api import generateInputs, run, parseOutput

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")
celery.conf.task_routes = {"create_pidc_task": {"queue": 'pidc'}}

@celery.task(name="create_pidc_task")
def create_pidc_task(zenodo_id):
    inputs = generateInputs(zenodo_id)
    res = run(inputs)
    output = parseOutput(res)
    return output
