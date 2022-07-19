# Класс для работы с логами

from os import path
from time import time, strftime, localtime


class Logs:

    def __init__(self):
        self.last_message = ''

    def post(self, *args: str):
        try:
            post = ' '.join(args)
            dt = strftime('%y-%m-%d %H:%M:%S', localtime(time()))

            mode = 'wt' if not path.exists('logs.txt') else 'at'
            self.last_message = dt + ' ' + post

            with open('logs.txt', mode) as f:
                f.write(self.last_message + '\n')

        except Exception as e:
            print('Logs')
            print(vars(e), e.args)
            print(e)
