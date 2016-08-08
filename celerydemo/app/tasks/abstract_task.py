import logging
from celerydemo.celery import app

class AbstractTask(app.Task):

    # required to keep this abstract class from the task registry
    abstract = True

    def __init__(self):
        self.log = logging.getLogger('django')

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Called after the task returns
        :param status:
        :param retval:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo:
        :return:
        """
        self.log.info('Task [{0}] returned with status [{0}]'.format(task_id, status))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        Called if a task fails
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo:
        :return:
        """

        self.log.error('Task [{0}] failed due to exception [{1}]'.format(task_id, exc))


    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """
        Called if a task is commanded to retry
        :param exc:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo:
        :return:
        """
        self.log.info('Task [{0}] set to retry'.format(task_id))

    def on_success(self, retval, task_id, args, kwargs):
        """
        Called on successful execution.  Overlaps with the signal decorator @task_success
        :param self:
        :param retval:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        self.log.info('Task [{0}] successfully executed'.format(task_id))