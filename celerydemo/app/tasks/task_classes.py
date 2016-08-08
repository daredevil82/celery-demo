import logging
import sys
from datetime import datetime

from .abstract_task import AbstractTask

class FactorialTask(AbstractTask):
    def __init__(self):
        self.log = logging.getLogger('django')

    def run(self, factor):
        """
        Class based version of the factorial function task
        :param factor:
        :return:
        """

        task_start = datetime.now()

        if factor is None or factor < 0:
            self.log.info('Negative or null numbers can\'t be factored')
            return -sys.maxsize - 1
        elif factor == 0:
            return 1
        else:
            result = 1
            for i in range(2, factor + 1):
                result += i

            self.log.info('Factorial elapsed time: {0}'.format(datetime.now() - task_start))
            return {'factorial': result}
