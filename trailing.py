# Класс для работы трейлинг стопа

from time import time


class TrailingStop:
    """Класс ведет контроль движения цены и рсчет трейлинг стопа

    """
    def __init__(self):
        """Инициализация объекта класса."""

        # Хранилище цен
        self.kline = list()

        # контрольная цена за период
        self.max_price = 0.0

        # интервал контроля цены трейлинг стопа
        self.stop_interval = 0.0

    def check(self, price: float):
        """Проверка цены.
        На входе функция получает последнюю цену price (float).
        На выходе получаем рекомендацию по активации стопа True/False.

        """

        # Создаем кортеж время-цена и добавляем его в хранилище цен
        item = (time(), price)
        self.kline.append(item)

        # Определяем индекс элемента с устаревшими данными
        j = 0
        for i in range(len(self.kline)):
            if self.kline[i][0] < (time() - self.stop_interval):
                j = i
                break

        # Удаляем данные, которые находятся за пределами необходимого периода
        # и не участвуют в расчетах, т.е. все что ранее j-го элемента
        self.kline = self.kline[j:]

        # Получаем контрольную цену
        stop_price = min([item[1] for item in self.kline])

        # Сравниваем цену с записанной в объекте, если цена растет,
        # то обновляем цену и возвращаем False, Если цена падает, возвращаем True
        if stop_price > self.max_price:
            self.max_price = stop_price
            return False
        return True

    def update(self, data: dict):
        """Обновление свойств класса.

        На входе получаем словарь {key:value}, где key - свойство объекта класса,
        а value - его новое значение.

        """
        for key in data.keys():
            if key in vars(self).keys():
                setattr(self, key, data[key])

    def reset(self):
        """обнуление / сброс данных стратегии."""
        self.max_price = 0.0
        self.kline = list()
