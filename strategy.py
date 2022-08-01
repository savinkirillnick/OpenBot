# Класс работы со стратегией


from item import DefaultItem


class Strategy:
    """Общий класс по работе со стратегиями"""
    def __init__(self, mode: str):
        try:
            self.cur = eval('Strategy'+mode.capitalize()+'()')
        except Exception as e:
            print(e.args)
            quit()

    def reset(self):
        self.cur.reset()

    def buy(self, price: float, qty: float):
        self.cur.buy(price, qty)

    def sell(self, price: float, qty: float):
        self.cur.sell(price, qty)

    def check(self, last_price: float):
        return self.cur.check(last_price)


class StrategySniper(DefaultItem):
    """Класс работы стратегии Sniper.

    buy_price - Цена покупки, ниже которой бот будет покупать в USDT;
    buy_lot - Объем лота к покупке в USDT;
    sell_price - Цена покупки, выше которой бот будет покупать в USDT;
    sell_lot - Объем лота к продаже в USDT;
    deposit - Депозит, выделяемый на работу бота в USDT;
    deposit_available - Депозит, определяемый ботом для торговли,
    при первоначальных настройках задаем равный deposit, при работе
    бота, он будет сам его корректировать.

    """
    def __init__(self):
        """Инициализация объекта класса."""

        # Цена покупки, ниже которой бот будет покупать
        self._buy_price = 0.0

        # Размер объема лота к покупке (в котируемой валюте USDT)
        self._buy_lot = 0.0

        # Цена продажи, выше которой бот будет продавать
        self._sell_price = 0.0

        # Размер объема лота к продаже (в котируемой валюте USDT)
        self._sell_lot = 0.0

        # Размер депозита, выделяемого на торговлю (USDT)
        self._deposit = 0.0

        # Размер депозита, доступного для торгов из выделенного (USDT)
        self._deposit_available = 0.0

        # Настройка трейлинг стопа, если False, то трейлинг отключен
        self.trailing_stop = False

        # Период следования трейлинг стопа в секундах
        self._trailing_stop_period = 0.0

        # Загрузка настроек из файла, если он есть
        self.load()

    def __str__(self):
        """Вывод информации о классе."""
        return f'Класс для работы со стратегией Sniper'

    def reset(self):
        """обнуление / сброс данных стратегии."""
        self.deposit_available = self.deposit

    def buy(self, price: float, qty: float):
        """Покупка / набор позиции в стратегии. Стратегия вычисляет размер
        доступного депозита.

        Функция на вход принимает:
        price (float) - цена покупки;
        qty (float) - объем покупки.

        """
        self.deposit_available -= price * qty
        if self.deposit_available < 0.0:
            self.deposit_available = 0.0

        self.save()

    def sell(self, price: float, qty: float):
        """Продажа / закрытие позиции в стратегии. Стратегия вычисляет размер
        доступного депозита.

        Функция на вход принимает:
        price (float) - цена продажи;
        qty (float) - объем продажи.

        """
        self.deposit_available += price * qty
        if self.deposit_available > self.deposit:
            self.reset()

        self.save()

    def check(self, last_price: float):
        """Проверка последней цены валюты с параметрами стратегии.

        Функция на вход принимает значение последней торгуемой цены last_price.

        Функция на выходе выдает кортеж из трех элементов:
        action (str) - действие, которое следует принять (buy, sell, wait)
        price (float) - цена покупки/продажи
        qty (float) - объем покупки/продажи"""
        if 0 < last_price <= self.buy_price:
            qty = self.buy_lot / last_price
            return 'buy', last_price, qty
        if 0 < self.sell_price <= last_price:
            qty = self.sell_lot / last_price
            return 'sell', last_price, qty

        return 'wait', 0.0, 0.0

    @property
    def buy_price(self):
        return self._buy_price

    @buy_price.setter
    def buy_price(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._buy_price = new_value

    @property
    def buy_lot(self):
        return self._buy_lot

    @buy_lot.setter
    def buy_lot(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._buy_lot = new_value

    @property
    def sell_price(self):
        return self._sell_price

    @sell_price.setter
    def sell_price(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._sell_price = new_value

    @property
    def sell_lot(self):
        return self._sell_lot

    @sell_lot.setter
    def sell_lot(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._sell_lot = new_value

    @property
    def deposit(self):
        return self._deposit

    @deposit.setter
    def deposit(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._deposit = new_value

    @property
    def deposit_available(self):
        return self._deposit_available

    @deposit_available.setter
    def deposit_available(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._deposit_available = new_value

    @property
    def trailing_stop_period(self):
        return self._trailing_stop_period

    @trailing_stop_period.setter
    def trailing_stop_period(self, new_value: float):
        DefaultItem.check_positive_value(new_value)
        self._trailing_stop_period = new_value
