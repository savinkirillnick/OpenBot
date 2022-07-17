# Класс пользовательских настроек бота


class BotSettings:

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

        # Обновление настроек, если они были заданы
        if data:
            self.update(data)

    def __str__(self):
        # Вывод информации о классе
        return f'Класс для работы с настройками бота'

    def get_items(self):
        # Получение словаря из всех свойств объекта и их названий
        data = {key: value.replace('_', ' ').capitalize() for key, value in zip(vars(self).keys(), vars(self).keys())}
        return data

    def update(self, data: dict):
        # обновление настроек бота
        for key in data.keys():
            if key in vars(self).keys():
                setattr(self, key, data[key])
