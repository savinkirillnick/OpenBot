# Класс для работы с логами

from os import path
from time import time, strftime, localtime


class Logs:
    """Класс работы с логами. Сохраняет лог в файл. Хранит последнюю запись
    в переменной last_message. Выводит лог на экран

    """
    def __init__(self):
        self.logs_journal = []
        self.post('Bot opened')

    def post(self, *args: str):
        try:
            post = ' '.join(args)
            dt = strftime('%y-%m-%d %H:%M:%S', localtime(time()))

            mode = 'wt' if not path.exists('logs.txt') else 'at'
            new_message = dt + ' ' + post
            self.logs_journal.append(new_message)
            print(new_message)

            with open('logs.txt', mode) as f:
                f.write(new_message + '\n')

        except Exception as e:
            print('Logs')
            print(vars(e), e.args)
            print(e)

    @property
    def last_message(self):
        return len(self.logs_journal), self.logs_journal[-1]

    @last_message.setter
    def last_message(self, _):
        return
