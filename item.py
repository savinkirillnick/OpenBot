# Родительский класс работы с объектами

import json
import traceback


def get_name():
    stack = traceback.extract_stack()
    return '{}'.format(stack[-2][2])


class DefaultItem:

    def __int__(self):
        pass

    def error(self, name):
        return 'Error. Class: ' + type(self).__name__ + '. Func: ' + name + '.'

    def update(self, data: dict):
        # обновление свойств класса
        for key in data.keys():
            if key in vars(self).keys():
                setattr(self, key, data[key])

    def get_item_names(self):
        # Получение словаря из всех свойств объекта и их названий
        data = {key: value.replace('_', ' ').capitalize() for key, value in zip(vars(self).keys(), vars(self).keys())}
        return data

    def save(self):
        # Сохранения данных объекта в файл
        # Преобразование всех свойств объекта в JSON формат, и запись в файл
        try:
            with open(type(self).__name__ + '.txt', 'w') as f:
                f.write(json.dumps(vars(self)) + '\n')
        except Exception as e:
            print(self.error(get_name()))
            print(vars(e), e.args)
            print(e)

    def load(self):
        # Загрузка данных объекта из файла
        # Загрузка JSON формата, расшифровка его и передача в функцию Update
        try:
            with open(type(self).__name__ + '.txt', 'r') as f:
                for line in f:
                    self.update(json.loads(line))
        except Exception as e:
            print(self.error(get_name()))
            print(vars(e), e.args)
            print(e)
