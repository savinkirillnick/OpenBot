# Класс пользовательских настроек бота

from item import DefaultItem


class BotSettings(DefaultItem):
    """
    Класс для работы с основными настройками бота, наследование от DefaultItem.

    api_key - Апи ключ от аккаунта биржи;
    api_secret - Секретный Апи ключ от аккаунта биржи;
    api_password - Пароль или третий ключ от аккаунта биржи (применяется на некоторых биржах);
    exchange - наименование биржи;
    pair - торговая пара;
    deposit - депозит, который выделяем боту для торговли в USDT;
    order_life - Время, через которое ордер отменяется и отправляется новый, в секундах;
    pause - Время паузы между отправками новых ордеров, в секундах;
    update_time - Время шага цикла программы, в секундах;
    strategy - стратегия по которой будет работать бот.

    """
    def __init__(self):
        """Инициализация объекта класса."""

        # API-ключ биржи
        self.api_key = ''

        # API-секрет биржи
        self.api_secret = ''

        # API-ключ дополнительный
        self.api_password = ''

        # Биржа
        self.exchange = ''

        # Торгуемая пара
        self.pair = ''

        # Депозит, выделяемый на торговлю, USDT
        self.deposit = 0.0

        # Время жизни ордера до отмены, сек
        self.order_life = 0.0

        # Время паузы между отправки ордеров, сек
        self.pause = 0.0

        # Время обновления запроса на биржу, сек
        self.update_time = 1.0

        # Стратегия, по которой будет работать бот
        self.strategy = 'sniper'

        # Комиссия за сделку биржи, в %
        self.fee = 0.0

        # Загрузка настроек из файла, если он есть
        self.load()

    def __str__(self):
        """Вывод информации о классе."""
        return f'Класс для работы с настройками бота'

    @staticmethod
    def check_value(value: float):
        if value < 0.0:
            raise Exception

    @property
    def deposit(self):
        return self.deposit

    @deposit.setter
    def deposit(self, new_value):
        DefaultItem.check_positive_value(new_value)
        self.deposit = new_value

    @property
    def order_life(self):
        return self.order_life

    @order_life.setter
    def order_life(self, new_value):
        DefaultItem.check_positive_value(new_value)
        self.order_life = new_value

    @property
    def pause(self):
        return self.pause

    @pause.setter
    def pause(self, new_value):
        DefaultItem.check_positive_value(new_value)
        self.pause = new_value

    @property
    def update_time(self):
        return self.update_time

    @update_time.setter
    def update_time(self, new_value):
        DefaultItem.check_positive_value(new_value)
        self.update_time = new_value

    @property
    def fee(self):
        return self.fee

    @fee.setter
    def fee(self, new_value):
        DefaultItem.check_positive_value(new_value)
        self.fee = new_value
