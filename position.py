# Класс работы с набором позиций

from item import DefaultItem


class Position(DefaultItem):
    """Класс для работы с позицией. Объект - это набранная позиция.

    В объекте хранятся:
    start_price - стартовая цена открытия позиции;
    take_profit - цена тейк профита;
    price - усредненная цена позиции;
    qty - объем позиции;
    timestamp - время создания позиции в формате Timestamp.

    Доступны функции:
    buy - Набор позициии в результате покупки;
    sell - Закрытие позиции в результате продажи;
    reset - Обнуление позиции.

    """
    def __init__(self):
        """Инициализация объекта класса"""

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

        # Загрузка настроек из файла, если он есть
        self.load()

    def __str__(self):
        """Вывод информации о классе."""
        return f'Класс для работы с позицией'

    def reset(self):
        """обнуление / сброс позиции."""
        self.price = 0.0
        self.qty = 0.0

    def buy(self, price: float, qty: float):
        """Покупка / набор позиции.

        Функция на вход принимает:
        price (float) - цена покупки;
        qty (float) - объем покупки.

        """
        lot = self.price * self.qty + price * qty
        self.qty += qty
        self.price = lot / self.qty
        self.save()

    def sell(self, price: float, qty: float):
        """Продажа / закрытие позиции.

        Функция на вход принимает:
        price (float) - цена продажи;
        qty (float) - объем продажи.

        """
        self.qty -= qty
        if round(self.qty, 8) <= 0:
            self.reset()

        self.save()
