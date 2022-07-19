# Класс работы со стратегией


from item import DefaultItem


class Sniper(DefaultItem):

    def __init__(self, data: dict):
        # Инициализация объекта класса

        # Цена покупки, ниже которой бот будет покупать
        self.buy_price = 0.0

        # Размер объема лота к покупке (в котируемой валюте USDT)
        self.buy_lot = 0.0

        # Цена продажи, выше которой бот будет продавать
        self.sell_price = 0.0

        # Размер объема лота к продаже (в котируемой валюте USDT)
        self.sell_lot = 0.0

        # Размер депозита, выделяемого на торговлю (USDT)
        self.deposit = 0.0

        # Размер депозита, доступного для торгов из выделенного (USDT)
        self.deposit_available = 0.0

        # Обновление настроек
        self.update(data)

    def __str__(self):
        # Вывод информации о классе
        return f'Класс для работы со стратегией Sniper'

    def reset(self):
        self.deposit_available = self.deposit

    def buy(self, price: float, qty: float):
        self.deposit_available -= price * qty
        if self.deposit_available < 0.0:
            self.deposit_available = 0.0

    def sell(self, price: float, qty: float):
        self.deposit_available += price * qty
        if self.deposit_available > self.deposit:
            self.reset()

    def check(self, last_price: float):

        pass
