# Класс работы бота с контролем параметров
import traceback
from math import log10
from time import time, sleep

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

        # API
        self.api = None

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

    def init_api(self):

        # Правила биржи
        self.rules = self.api.load_markets()

        # Монеты и пары биржи
        self.coins = set()
        self.pairs = set()

        for symbol in self.rules:
            if 'type' in self.rules[symbol]:
                if self.rules[symbol]['type'] != 'spot':
                    break
            base_asset = self.rules[symbol]['base'].lower()
            quote_asset =self.rules[symbol]['quote'].lower()
            pair = base_asset + '_' + quote_asset
            self.coins.add(base_asset)
            self.coins.add(quote_asset)
            self.pairs.add(pair)

            self.rules[pair] = {}
            self.rules[pair]['symbol'] = symbol
            if 'limits' in self.rules[symbol]:
                if 'price' in self.rules[symbol]['limits']:
                    if 'min' in self.rules[symbol]['limits']['price']:
                        self.rules[pair]['min_price'] = float(self.rules[symbol]['limits']['price']['min']) if \
                            isinstance(self.rules[symbol]['limits']['price']['min'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['min_price'] = 0.0
                    if 'max' in self.rules[symbol]['limits']['price']:
                        self.rules[pair]['max_price'] = float(self.rules[symbol]['limits']['price']['max']) if \
                            isinstance(self.rules[symbol]['limits']['price']['max'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['max_price'] = 0.0
                else:
                    self.rules[pair]['min_price'] = 0.0
                    self.rules[pair]['max_price'] = 0.0
                if 'amount' in self.rules[symbol]['limits']:
                    if 'min' in self.rules[symbol]['limits']['amount']:
                        self.rules[pair]['min_qty'] = float(self.rules[symbol]['limits']['amount']['min']) if \
                            isinstance(self.rules[symbol]['limits']['amount']['min'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['min_qty'] = 0.0
                    if 'max' in self.rules[symbol]['limits']['amount']:
                        self.rules[pair]['max_qty'] = float(self.rules[symbol]['limits']['amount']['max']) if \
                            isinstance(self.rules[symbol]['limits']['amount']['max'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['max_qty'] = 0.0
                else:
                    self.rules[pair]['min_qty'] = 0.0
                    self.rules[pair]['max_qty'] = 0.0
                if 'cost' in self.rules[symbol]['limits']:
                    if 'min' in self.rules[symbol]['limits']['cost']:
                        self.rules[pair]['min_cost'] = float(self.rules[symbol]['limits']['cost']['min']) if \
                            isinstance(self.rules[symbol]['limits']['cost']['min'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['min_cost'] = 0.0
                    if 'max' in self.rules[symbol]['limits']['cost']:
                        self.rules[pair]['max_cost'] = float(self.rules[symbol]['limits']['cost']['max']) if \
                            isinstance(self.rules[symbol]['limits']['cost']['max'], (int, float)) else 0.0
                    else:
                        self.rules[pair]['max_cost'] = 0.0
                else:
                    self.rules[pair]['min_cost'] = 0.0
                    self.rules[pair]['max_cost'] = 0.0
            else:
                self.rules[pair]['min_price'] = 0.0
                self.rules[pair]['max_price'] = 0.0
                self.rules[pair]['min_qty'] = 0.0
                self.rules[pair]['max_qty'] = 0.0
                self.rules[pair]['min_cost'] = 0.0
                self.rules[pair]['max_cost'] = 0.0

            if 'precision' in self.rules[symbol]:
                if 'price' in self.rules[symbol]['precision']:
                    self.rules[pair]['around_price'] = int(self.rules[symbol]['precision']['price']) if \
                        isinstance(self.rules[symbol]['precision']['price'], int) else \
                        int(abs(log10(float(self.rules[symbol]['precision']['price']))))
                else:
                    self.rules[pair]['around_price'] = 8
                if 'amount' in self.rules[symbol]['precision']:
                    self.rules[pair]['around_qty'] = int(self.rules[symbol]['precision']['amount']) if \
                        isinstance(self.rules[symbol]['precision']['amount'], int) else \
                        int(abs(log10(float(self.rules[symbol]['precision']['amount']))))
                else:
                    self.rules[pair]['around_qty'] = 8
            else:
                self.rules[pair]['around_price'] = 8
                self.rules[pair]['around_qty'] = 8

    def update_prices(self):
        sleep(1.0)

        while True:
            sleep(self.bot.update_time)

            try:
                raw_data = self.api.fetch_tickers()
            except Exception as e:
                raw_data = None
                self.log.post('* Get prices error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

            try:
                if isinstance(raw_data, dict):
                    for symbol in raw_data:
                        if isinstance(raw_data[symbol], dict):
                            if 'close' in raw_data[symbol]:
                                self.last_price = raw_data[symbol]['close']
                            else:
                                self.last_price = 0.0
            except Exception as e:
                self.log.post('* Raw data error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

    def update_strategies(self):
        pass

    def check_order(self):
        while True:
            try:
                if ttimer.check(time()):
                    get_orders()
                    check_orders()
                    if len(self.orders) > 0 and self.queue_id != '':
                        cancel_order(self.queue_id)
                    else:
                        self.queue_id = ''
                    sleep(10)
                else:
                    sleep(1)
            except Exception as e:
                self.log.post('* Update order error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

    def update_activity(self):
        pass

