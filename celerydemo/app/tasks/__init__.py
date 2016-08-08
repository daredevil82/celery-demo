from celerydemo.celery import app

import logging

from celery.signals import task_prerun, task_postrun, task_revoked, task_success, task_retry, task_failure

log = logging.getLogger('django')

def kwarg_out(**kwargs):
    for k, v in kwargs.items():
        log.info('\t{0}:\t{1}'.format(k, v))

# @task_prerun.connect()
# def on_prerun(**kwargs):
#     log.info('Task PreRun signal called with args: ')
#     kwarg_out(**kwargs)
#
# @task_postrun.connect()
# def on_postrun(**kwargs):
#     log.info('Task PostRun signal called with args: ')
#     kwarg_out(**kwargs)
#
# @task_failure.connect()
# def on_failure(**kwargs):
#     log.info('Task Failure signal called with args: ')
#     kwarg_out(**kwargs)
#
# @task_revoked.connect()
# def on_revoke(**kwargs):
#     log.info('Task Revoked signal called with args: ')
#     kwarg_out(**kwargs)
#
# @task_success.connect()
# def on_success(**kwargs):
#     log.info('Task Success signal called with args: ')
#     kwarg_out(**kwargs)
#
# @task_retry.connect()
# def on_retry(**kwargs):
#     log.info('Task Retry signal called with args: ')
#     kwarg_out(**kwargs)