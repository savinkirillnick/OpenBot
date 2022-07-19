# Класс пользовательских настроек бота

from item import DefaultItem


class BotSettings(DefaultItem):

    def __init__(self, data: dict):
        # Инициализация объекта класса

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

        # Обновление настроек, если они были заданы
        if data:
            self.update(data)

    def __str__(self):
        # Вывод информации о классе
        return f'Класс для работы с настройками бота'
