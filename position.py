# Класс работы с набором позиций

from item import DefaultItem


class Position(DefaultItem):

    def __init__(self, data: dict):
        # Инициализация объекта класса

        # Начальная цена позиции
        self.start_price = 0.0

        # Цена тейк профита позиции
        self.take_profit = 0.0

        # Цена позиции
        self.price = 0.0

        # Объем позиции
        self.qty = 0.0

        # дата создания позиции
        self.timestamp = 0.0

        # Обновление настроек
        self.update(data)

    def __str__(self):
        # Вывод информации о классе
        return f'Класс для работы с позицией'

    def reset(self):
        # обнуление / сброс позиции
        self.price = 0.0
        self.qty = 0.0

    def buy(self, price, qty):
        # Покупка / набор позиции
        lot = self.price * self.qty + price * qty
        self.qty += qty
        self.price = lot / self.qty

    def sell(self, price, qty):
        # Продажа / закрытие позиции
        self.qty -= qty
        if round(self.qty, 8) <= 0:
            self.reset()
