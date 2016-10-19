from functools import wraps

from celery.utils.log import get_task_logger

from myproject.celeryconf import app
from .models import Job

logger = get_task_logger(__name__)


def update_job(fn):
    @wraps(fn)
    def wrapper(job_id, *args, **kwargs):
        logger.info("Inside of wrapper")
        job = Job.objects.get(id=job_id)
        job.status = 'started'
        job.save()
        try:
            result = fn(*args, **kwargs)
            job.result = result
            job.status = 'finished'
            job.save()
        except:
            job.result = None
            job.status = 'failed'
            job.save()
    return wrapper


@app.task
@update_job
def power(n):
    logger.info("Inside of power")
    """Return 2 to the n'th power"""
    return 2 ** n


@app.task
@update_job
def fib(n):
    logger.info("Inside of fib")
    """Return the n'th Fibonacci number.
    """
    if n < 0:
        raise ValueError("Fibonacci numbers are only defined for n >= 0.")
    return _fib(n)


def _fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return _fib(n - 1) + _fib(n - 2)

TASK_MAPPING = {
    'power': power,
    'fibonacci': fib
}
