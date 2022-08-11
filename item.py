# Родительский класс работы с объектами

import json
import traceback
from os.path import exists


def get_name():
    stack = traceback.extract_stack()
    return '{}'.format(stack[-2][2])


class DefaultItem:
    """Родительский класс для классов BotSettings, Position, Strategy.

    В данном классе описаны основные функции, которые необходимы для
    нормальной работы всех дочерних классов. Это обновление свойств класса,
    Получение словаря из свойств и их названий, сохранение в файл и загрузка
    из файла данных объекта класса.

    """

    def __int__(self):
        """Инициализация пустого объекта. """
        pass

    def error(self, name: str):
        """Возврат места нахождения ошибки, откуда она была вызвана."""
        return 'Error. Class: ' + type(self).__name__ + '. Func: ' + name + '.'

    def update(self, data: dict):
        """Обновление свойств класса.

        На входе получаем словарь {key:value}, где key - свойство объекта класса,
        а value - его новое значение.

        """
        for key in data.keys():
            if key in vars(self).keys():
                setattr(self, key, data[key])
        self.save()

    def get_item_names(self):
        """Получение словаря из всех свойств объекта и их названий.
        функия возвращает словарь типа:
        {'api_key': 'Api key', 'exchange': 'Exchange', ... }"""
        data = {key if not key.startswith('_') else key.replace('_', '', 1): value.replace('_', ' ').capitalize() if
        not value.startswith(
            '_') else value.replace('_', '', 1).replace('_', ' ').capitalize() for
                key, value in zip(vars(self).keys(), vars(self).keys())}

        return data

    def get_item_types(self):
        """Полчение вех типов переменных в виде словаря
        функия возвращает словарь типа:
        {'api_key': <class 'str'>, 'exchange': <class 'str'>, ... }"""
        data = {key if not key.startswith('_') else key.replace('_', '', 1): type(vars(self)[key]) for
                key in vars(self).keys()}

        return data

    def save(self):
        """Сохранения данных объекта в файл.
        Преобразование всех свойств объекта в JSON формат, и запись в файл.

        """
        try:
            with open(type(self).__name__ + '.txt', 'w') as f:
                f.write(json.dumps(vars(self)) + '\n')
        except Exception as e:
            print(self.error(get_name()))
            print(vars(e), e.args)
            print(e)

    def load(self):
        """Загрузка данных объекта из файла.
        Загрузка JSON формата, расшифровка его и передача в функцию Update.

        """
        if exists(type(self).__name__ + '.txt'):
            try:
                with open(type(self).__name__ + '.txt', 'r') as f:
                    for line in f:
                        self.update(json.loads(line))
            except Exception as e:
                print(self.error(get_name()))
                print(vars(e), e.args)
                print(e)
        else:
            self.save()

    @staticmethod
    def check_positive_value(value: float):
        if value < 0.0:
            raise Exception
