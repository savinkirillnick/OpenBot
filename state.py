# Класс работы бота с контролем параметров

from time import time

from settings import BotSettings
from position import Position
from logs import Logs
from strategy import Strategy


class BotState:
    """Класс для ведения и контроля циклов работы программы.
    В данном классе хранятся и обрабатываются все необходимые параметры.
    Все свойства класса являются перманентными и обнуляются при перезапуске программы.

    """
    def __init__(self):
        """Инициализация объекта класса."""

        # Флаг запущен бот или нет
        self.bot_is_run = False

        # Правила биржи
        self.rules = dict()

        # Монеты и пары биржи
        self.coins = set()
        self.pairs = set()

        # Балансы по монетам
        self.balances = dict()

        # Списки открытых ордеров и закрытых ордеров
        self.orders = list()
        self.trades = list()

        # Объект настроек бота
        self.bot = BotSettings()

        # Объект набранной позиции
        self.pos = Position()

        # Объект лог
        self.log = Logs()

        # Объект стратегии
        self.strategy = Strategy(vars(self.bot)['strategy'])

        # идентификатор ордера на отмену
        self.queue_id = ''
        # сторона ордера на отмену (buy/sell)
        self.queue_side = ''

        # Последняя цена
        self.last_price = 0.0

        # Разрешение на покупки и продажу
        self.buy_access = False
        self.sell_access = False

        # время последнего отправленного ордера
        self.last_trade_time = time()

        # Начальное время покупки и продажи
        self.start_buy_time = 0.0
        self.start_sell_time = 0.0

        # цены и объемы последних покупки и продажы
        self.buy_price = 0.0
        self.sell_price = 0.0
        self.buy_qty = 0.0
        self.sell_qty = 0.0

        # Корректировка времени биржи и времени машины
        self.exchange_delta_time = 0.0
