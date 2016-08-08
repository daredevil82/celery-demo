import logging
import sys

from datetime import datetime


from . import app

log = logging.getLogger('django')

@app.task(bind = True)
def subtract(self, x, y):
    return x - y


@app.task(bind = True)
def factorial(self, factor):

    """
    A very naive implementation of factorial
    :param self:
    :param factor:
    :return: -sys.maxsize - 1 if :param factor is 0.  1 if :param factor is 0, otherwise the factorial of the number
    """

    task_start = datetime.now()

    if factor is None or factor < 0:
        log.info('Negative or null numbers can\'t be factored')
        return -sys.maxsize - 1
    elif factor == 0:
        return 1
    else:
        result = 1
        for i in range(2, factor + 1):
            result += i

        log.info('Factorial elapsed time: {0}'.format(datetime.now() - task_start))
        return {'factorial': result}

