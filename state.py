# Класс работы бота с контролем параметров
import traceback
from math import log10, floor
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

        # Стакан
        self.depth = dict()
        self.depth['bids'] = list()
        self.depth['asks'] = list()

        # Балансы по монетам
        self.balances = dict()

        # Списки открытых ордеров и закрытых ордеров
        self.orders = list()
        self.trades = list()

        # Объект настроек бота
        self.bot = BotSettings()

        # Объект набранной позиции
        self.position = Position()

        # Объект лог
        self.log = Logs()

        # Объект стратегии
        self.strategy = Strategy(vars(self.bot)['strategy'])

        # идентификатор ордера на отмену
        self.queue_id = ''
        # сторона ордера на отмену (buy/sell)
        self.queue_side = ''

        # Список бирж
        self.exchanges = list()

        # Последняя цена
        self.last_price = 0.0

        # Время покупки и продажи
        self.last_buy_time = 0.0
        self.last_sell_time = 0.0

        # цены и объемы последних покупки и продажы
        self.buy_price = 0.0
        self.sell_price = 0.0
        self.buy_qty = 0.0
        self.sell_qty = 0.0

        # Корректировка времени биржи и времени машины
        self.exchange_delta_time = 0.0

        # Регулятор времени
        self.time_ctrl = floor(time())

    def init_api(self):

        # Правила биржи
        rules_raw = self.api.load_markets()

        # Монеты и пары биржи
        self.coins = set()
        self.pairs = set()

        # для каждого символа выбираем торговые правила
        for symbol in rules_raw:

            if 'type' in rules_raw[symbol] and rules_raw[symbol]['type'] != 'spot':
                # Если пара не спотовая, пропускаем
                break

            base_asset = rules_raw[symbol]['base'].lower()
            quote_asset = rules_raw[symbol]['quote'].lower()
            pair = base_asset + '_' + quote_asset

            # пополняем массивы данными о монетах и парах
            self.coins.add(base_asset)
            self.coins.add(quote_asset)
            self.pairs.add(pair)

            # Устанавливаем правила торговли на бирже
            self.rules[pair] = {}
            self.rules[pair]['symbol'] = symbol
            # минимальная цена сделки
            self.rules[pair]['min_price'] = float(rules_raw[symbol]['limits']['price']['min']) if \
                isinstance(rules_raw[symbol]['limits']['price']['min'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'price' in rules_raw[symbol]['limits'] and \
                'min' in rules_raw[symbol]['limits']['price'] else 0.0
            # максимальная цена сделки
            self.rules[pair]['max_price'] = float(rules_raw[symbol]['limits']['price']['max']) if \
                isinstance(rules_raw[symbol]['limits']['price']['max'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'price' in rules_raw[symbol]['limits'] and \
                'max' in rules_raw[symbol]['limits']['price'] else 0.0
            # минимальный объем сделки
            self.rules[pair]['min_qty'] = float(rules_raw[symbol]['limits']['amount']['min']) if \
                isinstance(rules_raw[symbol]['limits']['amount']['min'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'amount' in rules_raw[symbol]['limits'] and \
                'min' in rules_raw[symbol]['limits']['amount'] else 0.0
            # максимальный объем сделки
            self.rules[pair]['max_qty'] = float(rules_raw[symbol]['limits']['amount']['max']) if \
                isinstance(rules_raw[symbol]['limits']['amount']['max'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'amount' in rules_raw[symbol]['limits'] and \
                'max' in rules_raw[symbol]['limits']['amount'] else 0.0
            # минимальная сумма сделки
            self.rules[pair]['min_cost'] = float(rules_raw[symbol]['limits']['cost']['min']) if \
                isinstance(rules_raw[symbol]['limits']['cost']['min'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'cost' in rules_raw[symbol]['limits'] and \
                'min' in rules_raw[symbol]['limits']['cost'] else 0.0
            # максимальная сумма сделки
            self.rules[pair]['max_cost'] = float(rules_raw[symbol]['limits']['cost']['max']) if \
                isinstance(rules_raw[symbol]['limits']['cost']['max'], (int, float)) and \
                'limits' in rules_raw[symbol] and 'cost' in rules_raw[symbol]['limits'] and \
                'max' in rules_raw[symbol]['limits']['cost'] else 0.0
            # округление цены сделки
            self.rules[pair]['around_price'] = int(rules_raw[symbol]['precision']['price']) if \
                isinstance(rules_raw[symbol]['precision']['price'], int) and \
                'precision' in rules_raw[symbol] and 'price' in rules_raw[symbol]['precision'] else \
                int(abs(log10(float(rules_raw[symbol]['precision']['price'])))) if \
                    isinstance(rules_raw[symbol]['precision']['price'], float) and \
                    'precision' in rules_raw[symbol] and 'price' in rules_raw[symbol]['precision'] else 8
            # округление объема сделки
            self.rules[pair]['around_qty'] = int(rules_raw[symbol]['precision']['amount']) if \
                isinstance(rules_raw[symbol]['precision']['amount'], int) and \
                'precision' in rules_raw[symbol] and 'amount' in rules_raw[symbol]['precision'] else \
                int(abs(log10(float(rules_raw[symbol]['precision']['amount'])))) if \
                    isinstance(rules_raw[symbol]['precision']['amount'], float) and \
                    'precision' in rules_raw[symbol] and 'amount' in rules_raw[symbol]['precision'] else 8

    @property
    def check_time(self):
        if self.time_ctrl == floor(time()):
            return False
        else:
            self.time_ctrl = floor(time())
            return True

    def get_orders(self):

        try:
            orders = self.api.fetch_open_orders(self.rules[self.bot.pair]['symbol'])
        except Exception as e:
            self.log.post('* Get orders error. ' + str(type(e).__name__) + ': ' + str(e))
            self.log.post('** Ошибка:\n' + traceback.format_exc())
            orders = list()
        if orders:
            self.orders = orders
        else:
            self.orders = list()

    def get_trades(self):

        try:
            trades = self.api.fetch_my_trades(self.rules[self.bot.pair]['symbol'])
        except Exception as e:
            self.log.post('* Get trades error. ' + str(type(e).__name__) + ': ' + str(e))
            self.log.post('** Ошибка:\n' + traceback.format_exc())
            trades = list()
        if trades:
            self.trades = trades
        else:
            self.trades = list()

    def check_orders(self):
        if len(self.orders) > 0:
            current_time = time()
            try:
                for i in range(len(self.orders)):
                    if self.orders[i]['timestamp'] / 1000 + self.bot.order_life < current_time:
                        self.queue_id = self.orders[i]['id']
                        self.queue_side = self.orders[i]['side']
            except Exception as e:
                self.log.post('* Check orders error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())
        else:
            self.queue_id = ''
            self.queue_side = ''

    def cancel_order(self, order_id=''):
        id = order_id if order_id != '' else self.queue_id if self.queue_id != '' else ''
        if id != '':
            try:
                cancel = self.api.cancel_order(id, self.rules[self.bot.pair]['symbol'])
            except Exception as e:
                self.log.post('* Cancel order error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())
                cancel = 0
            if cancel:
                self.log.post('Order canceled')
                self.queue_id = ''

                # Обнуляем время той стороны, которой отменили ордер
                if self.queue_side.lower() == 'buy':
                    self.last_buy_time = 0.0
                elif self.queue_side.lower() == 'sell':
                    self.last_sell_time = 0.0
                self.queue_side = ''

                for i in range(len(self.orders)):
                    if self.orders[i]['id'] == id:
                        del self.orders[i]
                        break

    @staticmethod
    def ff(d: float, n: int):
        return ('{:.%df}' % n).format(d)

    def check_trade_rules(self, price: float, qty: float):
        # Проверяем соответсвие ордера правилам биржи
        try:
            # Проверяем, существует ли правило, и не нарушиют ли параметры сделки данные правила
            if price < self.rules[self.bot.pair]['min_price']:
                self.log.post(self.bot.pair + ' error: Price < Min')
                return False
            if qty < self.rules[self.bot.pair]['min_qty']:
                self.log.post(self.bot.pair + ' error: Qty < Min')
                return False
            if qty * price < self.rules[self.bot.pair]['min_sum']:
                self.log.post(self.bot.pair + ' error: Cost < Min')
                return False
            if 0 < self.rules[self.bot.pair]['max_price'] < price:
                self.log.post(self.bot.pair + ' error: Price > Max')
                return False
            if 0 < self.rules[self.bot.pair]['max_qty'] < qty:
                self.log.post(self.bot.pair + ' error: Qty > Max')
                return False
            if 0 < self.rules[self.bot.pair]['max_sum'] < qty * price:
                self.log.post(self.bot.pair + ' error: Cost > Max')
                return False
        except Exception as e:
            print('Check rules error')
            print(vars(e), e.args)
            print(e)
            self.log.post('Check rules error')
            return False

        # Если нарушений правил нет, выводим True
        return True

    def prep_price(self, pair: str, price: float):
        # форматируем цену
        around_price = self.rules[pair]['around_price']
        return self.ff(price, around_price)

    def prep_qty(self, pair: str, qty: float):
        # форматируем объем
        around_qty = self.rules[pair]['around_qty']
        round_qty = float(self.ff(qty, around_qty))
        if round_qty > qty:
            while round_qty > qty:
                round_qty -= 0.1 ** around_qty
        return self.ff(round_qty, around_qty)

    def buy(self, price: float, qty: float):
        # обработка покупки
        self.buy_price = price
        self.buy_qty = qty
        self.last_buy_time = time()
        self.strategy.buy(price, qty)
        self.position.buy(price, qty)

    def sell(self, price: float, qty: float):
        # обработка продажи
        self.sell_price = price
        self.sell_qty = qty
        self.last_sell_time = time()
        self.strategy.sell(price, qty)
        self.position.sell(price, qty)

    def update_depth(self):

        while True:
            sleep(self.bot.update_time)

            try:
                depth = self.api.fetch_order_book(self.rules[self.bot.pair]['symbol'], None)
            except Exception as e:
                self.log.post('* Get depth error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())
                depth = dict()
            if depth:
                self.depth = depth

    def update_prices(self):

        while True:
            sleep(self.bot.update_time)

            try:
                raw_data = self.api.fetch_tickers()
            except Exception as e:
                raw_data = None
                self.log.post('* Get prices error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

            try:
                if isinstance(raw_data, dict) and self.rules[self.bot.pair]['symbol'] in raw_data:
                    self.last_price = raw_data[self.rules[self.bot.pair]['symbol']]['close']
            except Exception as e:
                self.log.post('* Raw data error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

    def update_strategies(self):

        while True:
            sleep(self.bot.update_time)

            # Получаем действие, цену и объем при проверке стратегии
            if self.last_price:
                action, price, qty = self.strategy.check(self.last_price)
            else:
                action, price, qty = ('wait', 0.0, 0.0)

            pair = self.bot.pair
            order = dict()

            # Если пришло действие покупать или продавать, то отправляем соответствующий ордер
            try:
                if action == 'buy' and self.last_buy_time + self.bot.pause < time() and \
                        self.check_trade_rules(price, qty):
                    order = self.api.create_limit_buy_order(self.rules[pair]['symbol'], self.prep_qty(pair, qty),
                                                            self.prep_price(pair, price))
                elif action == 'sell' and self.last_sell_time + self.bot.pause < time() and \
                        self.check_trade_rules(price, qty):
                    order = self.api.create_limit_sell_order(self.rules[pair]['symbol'], self.prep_qty(pair, qty),
                                                             self.prep_price(pair, price))
            except Exception as e:
                self.log.post('* Send order error. ' + str(type(e).__name__) + ': ' + str(e))
                self.log.post('** Ошибка:\n' + traceback.format_exc())

            # Если ордер отправился и мы получили ответ обновляем данные в стратегии и позиции
            if action != 'wait' and order:
                if action == 'buy':
                    self.buy(price, qty)
                elif action == 'sell':
                    self.sell(price, qty)

    def update_order(self):
        while True:
            try:
                if self.check_time:
                    self.get_orders()
                    self.check_orders()
                    if len(self.orders) > 0 and self.queue_id != '':
                        self.cancel_order(self.queue_id)
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
