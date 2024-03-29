# Класс графического интерфейса

import tkinter as tk
import traceback
from time import strftime, localtime
from tkinter import ttk
from logs import Logs


# Список разделов программы
gui_menu = ['main',
            'depth',
            'orders',
            'trades',
            'terminal',
            'settings'
            ]


class MainWindow(tk.Frame):

    def __init__(self, root, bot_controller):
        super().__init__(root)

        self._root = root
        self._bc = bot_controller
        self.display_window = 'main'

        self.width_root = 420
        self.height_root = 480

        self._init_menu()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        self.log = Logs()

        self._init_main_window()

    def _init_menu(self):
        # Создаем меню
        self.menu_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=20)
        self.menu_bar.pack(side=tk.TOP, fill=tk.X)

        # создаем кнопки переключения окон
        for item in gui_menu:
            tk.Button(self.menu_bar, command=eval('self._init_' + item + '_window'), compound=tk.TOP,
                      bg='#ffffff', relief='flat', bd=0, activebackground='#dddddd',
                      text=item.capitalize()).pack(side=tk.LEFT, padx=5)

        # Основные кнопки управления программой
        self.start_stop_button = tk.Button(self.menu_bar, command=None, compound=tk.TOP, bg='#ccddff', relief='flat',
                                           bd=0, activebackground='#bbccff', text='Start')
        self.start_stop_button.pack(side=tk.LEFT, padx=5)

    def _init_main_window(self):
        # Создаем основное окно программы

        self.display_window = 'main'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        y = 5
        tk.Label(self.tool_bar, bg='#ffffff', text='LOGS:', font='Arial 10 bold').place(x=10, y=y)

        y = 25
        self.logs_box = tk.Text(self.tool_bar, font='Arial 10', wrap=tk.WORD, state='disabled')
        logs_scrollbar = tk.Scrollbar(self.logs_box)

        logs_scrollbar['command'] = self.logs_box.yview
        self.logs_box['yscrollcommand'] = logs_scrollbar.set

        self.logs_box.place(x=10, y=y, width=self.width_root-20, height=self.height_root-50)
        logs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._show_logs()

    def _show_logs(self, message=''):
        # Функция показа логов

        self.logs_box.configure(state='normal')
        self.logs_box.insert(tk.END, '\n'.join(self._bc.log.logs_journal)+'\n' if not message else message+'\n')
        self.logs_box.configure(state='disable')
        self.logs_box.yview_moveto(1)

    def insert_logs(self, message):
        self._bc.log.post(message)
        self._show_logs(message)

    def _init_depth_window(self):
        # Функция показа окна стакана

        self.display_window = 'depth'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(self.tool_bar, text='BIDS', bg='#ffffff', font='Arial 10 bold').place(x=10, y=5)
        tk.Label(self.tool_bar, text='ASKS', bg='#ffffff', font='Arial 10 bold').place(x=210, y=5)

        self.tree_depth = ttk.Treeview(self.tool_bar)
        self.tree_depth['columns'] = ('bid_price', 'bid_qty', 'bid_sum', 'ask_price', 'ask_qty', 'ask_sum',)
        self.tree_depth.column('#0', width=0, minwidth=0, stretch=tk.NO)
        self.tree_depth.column('bid_price', width=70, minwidth=70, stretch=tk.NO)
        self.tree_depth.column('bid_qty', width=70, minwidth=70, stretch=tk.NO)
        self.tree_depth.column('bid_sum', width=70, minwidth=70, stretch=tk.NO)
        self.tree_depth.column('ask_price', width=70, minwidth=70, stretch=tk.NO)
        self.tree_depth.column('ask_qty', width=70, minwidth=70, stretch=tk.NO)
        self.tree_depth.column('ask_sum', width=70, minwidth=70, stretch=tk.NO)

        self.tree_depth.heading('bid_price', text='Price', anchor=tk.W)
        self.tree_depth.heading('bid_qty', text='Qty', anchor=tk.W)
        self.tree_depth.heading('bid_sum', text='Sum', anchor=tk.W)
        self.tree_depth.heading('ask_price', text='Price', anchor=tk.W)
        self.tree_depth.heading('ask_qty', text='Qty', anchor=tk.W)
        self.tree_depth.heading('ask_sum', text='Sum', anchor=tk.W)

        self.tree_depth.place(x=0, y=30, width=self.width_root, height=self.height_root-35)

        self._view_tree()

    def _view_tree(self):
        # Заполнение и отображение стакана

        for i in self.tree_depth.get_children():
            self.tree_depth.delete(i)

        around_price = self._bc.rules[self._bc.bot.pair]['around_price']
        around_qty = self._bc.rules[self._bc.bot.pair]['around_qty']

        for i in range(min(len(self._bc.depth['bids']), len(self._bc.depth['asks']), 20)):

            self.tree_depth.insert('', 'end', 'depth_' + str(i), values=(
                self.ff(self._bc.depth['bids'][i][0], around_price),
                self.ff(self._bc.depth['bids'][i][1], around_qty),
                self.ff(self._bc.depth['bids'][i][0]*self._bc.depth['bids'][i][1], around_price),
                self.ff(self._bc.depth['asks'][i][0], around_price),
                self.ff(self._bc.depth['asks'][i][1], around_qty),
                self.ff(self._bc.depth['asks'][i][0]*self._bc.depth['asks'][i][1], around_price),
            ))

        self.after(int(self._bc.bot.update_time * 1000), self._view_tree)

    def _init_orders_window(self):
        # Функция показа окна с открытыми ордерами

        self.display_window = 'orders'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(self.tool_bar, text='ORDERS', bg='#ffffff', font='Arial 10 bold').place(x=10, y=5)

        ttk.Button(self.tool_bar, text='Cancel', command=self._init_cancel).place(x=self.width_root-80, y=5,
                                                                                  width=70, height=23)
        self.tree_orders = ttk.Treeview(self.tool_bar)

        self.tree_orders['columns'] = ('side', 'price', 'filled', 'amount', 'sum')
        self.tree_orders.column('#0', width=0, minwidth=0, stretch=tk.NO)
        self.tree_orders.column('side', width=84, minwidth=50)
        self.tree_orders.column('price', width=84, minwidth=50, stretch=tk.NO)
        self.tree_orders.column('filled', width=84, minwidth=50, stretch=tk.NO)
        self.tree_orders.column('amount', width=84, minwidth=50, stretch=tk.NO)
        self.tree_orders.column('sum', width=84, minwidth=50, stretch=tk.NO)

        self.tree_orders.heading('side', text='Side', anchor=tk.W)
        self.tree_orders.heading('price', text='Price', anchor=tk.W)
        self.tree_orders.heading('filled', text='Filled', anchor=tk.W)
        self.tree_orders.heading('amount', text='Amount', anchor=tk.W)
        self.tree_orders.heading('sum', text='Sum', anchor=tk.W)

        around_price = self._bc.rules[self._bc.bot.pair]['around_price']
        around_qty = self._bc.rules[self._bc.bot.pair]['around_qty']

        for i in range(len(self._bc.orders)):
            self.tree_orders.insert('', 'end', self._bc.orders[i]['id'], text=self._bc.orders[i]['id'],
                                    values=(self._bc.orders[i]['side'],
                                            self.ff(self._bc.orders[i]['price'], around_price), self.ff(
                                        (lambda x: 0.0 if x is None else x)(self._bc.orders[i]['filled']),
                                        around_qty), self.ff(
                                        (lambda x: 0.0 if x is None else x)(self._bc.orders[i]['filled']) + (
                                            lambda x: 0.0 if x is None else x)(self._bc.orders[i]['remaining']),
                                        around_qty), self.ff(
                                        self._bc.orders[i]['price'] * (lambda x: 0.0 if x is None else x)(
                                            self._bc.orders[i]['amount']), 8)))

        self.tree_orders.place(x=0, y=30, width=self.width_root, height=self.height_root-35)

    def _init_cancel(self):
        # Отмена ордера на кнопку

        self._bc.cancel_order(order_id=self.tree_orders.item(self.tree_orders.focus())['text'])

    def ff(self, d: float, n: int):
        # Форматирование числа до n-знака

        return self._bc.ff(d, n)

    def _init_trades_window(self):
        # Функция показа окна истории совершенных сделок

        self.display_window = 'trades'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(self.tool_bar, text='TRADES', bg='#ffffff', font='Arial 10 bold').place(x=10, y=5)

        self.tree_trades = ttk.Treeview(self.tool_bar)

        self.tree_trades['columns'] = ('time', 'side', 'price', 'amount', 'sum')
        self.tree_trades.column('#0', width=0, minwidth=0, stretch=tk.NO)
        self.tree_trades.column('time', width=90, minwidth=50, stretch=tk.NO)
        self.tree_trades.column('side', width=78, minwidth=40, stretch=tk.NO)
        self.tree_trades.column('price', width=84, minwidth=50, stretch=tk.NO)
        self.tree_trades.column('amount', width=84, minwidth=50, stretch=tk.NO)
        self.tree_trades.column('sum', width=84, minwidth=50, stretch=tk.NO)

        self.tree_trades.heading('time', text='Time', anchor=tk.W)
        self.tree_trades.heading('side', text='Side', anchor=tk.W)
        self.tree_trades.heading('price', text='Price', anchor=tk.W)
        self.tree_trades.heading('amount', text='Amount', anchor=tk.W)
        self.tree_trades.heading('sum', text='Sum', anchor=tk.W)

        around_price = self._bc.rules[self._bc.bot.pair]['around_price']
        around_qty = self._bc.rules[self._bc.bot.pair]['around_qty']

        self._bc.get_trades()

        for i in range(min(len(self._bc.trades), 20)):
            self.tree_trades.insert('', 'end', 'trades_' + str(i),
                                    values=(
                                    strftime('%m/%d %H:%M', localtime(self._bc.trades[i]['timestamp'] / 1000)),
                                    self._bc.trades[i]['side'],
                                    self.ff(self._bc.trades[i]['price'], around_price),
                                    self.ff((lambda x: 0.0 if x is None else x)(self._bc.trades[i]['amount']),
                                            around_qty),
                                    self.ff((lambda x: 0.0 if x is None else x)(self._bc.trades[i]['cost']),
                                            around_price)))

        self.tree_trades.place(x=0, y=30, width=self.width_root, height=self.height_root-35)

    def _init_terminal_window(self):
        # Функция показа окна ручной торговли

        self.display_window = 'terminal'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root - 20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        y = 5
        tk.Label(self.tool_bar, bg='#ffffff', text='FUNDS:', font='Arial 10 bold').place(x=10, y=y)

        y += 25
        self.quote_asset = tk.Label(self.tool_bar, bg='#ffffff', text='Quote')
        self.quote_asset.place(x=10, y=y)
        self.base_asset = tk.Label(self.tool_bar, bg='#ffffff', text='Base')
        self.base_asset.place(x=220, y=y)
        self.entry_quote = ttk.Entry(self.tool_bar)
        self.entry_quote.place(x=60, y=y, width=140)
        self.entry_base = ttk.Entry(self.tool_bar)
        self.entry_base.place(x=270, y=y, width=140)

        y += 25
        tk.Label(self.tool_bar, bg='#ffffff', text='BUY').place(x=10, y=y)
        self.label_buy_num_step = tk.Label(self.tool_bar, bg='#ffffff', text='Step')
        self.label_buy_num_step.place(x=60, y=y)
        tk.Label(self.tool_bar, bg='#ffffff', text='SELL').place(x=220, y=y)
        self.label_sell_num_step = tk.Label(self.tool_bar, bg='#ffffff', text='Step')
        self.label_sell_num_step.place(x=270, y=y)

        y += 25
        self.label_buy_price = tk.Label(self.tool_bar, bg='#ffffff', text='Price')
        self.label_buy_price.place(x=10, y=y)
        self.label_sell_price = tk.Label(self.tool_bar, bg='#ffffff', text='Price')
        self.label_sell_price.place(x=220, y=y)
        self.entry_buy_price = ttk.Entry(self.tool_bar)
        self.entry_buy_price.insert(0, '0')
        self.entry_buy_price.place(x=60, y=y, width=140)
        self.entry_sell_price = ttk.Entry(self.tool_bar)
        self.entry_sell_price.insert(0, '0')
        self.entry_sell_price.place(x=270, y=y, width=140)

        y += 25
        self.label_buy_qty = tk.Label(self.tool_bar, bg='#ffffff', text='Qty')
        self.label_buy_qty.place(x=10, y=y)
        self.label_sell_qty = tk.Label(self.tool_bar, bg='#ffffff', text='Qty')
        self.label_sell_qty.place(x=220, y=y)
        self.entry_buy_qty = ttk.Entry(self.tool_bar)
        self.entry_buy_qty.insert(0, '0')
        self.entry_buy_qty.place(x=60, y=y, width=140)
        self.entry_sell_qty = ttk.Entry(self.tool_bar)
        self.entry_sell_qty.insert(0, '0')
        self.entry_sell_qty.place(x=270, y=y, width=140)

        y += 25
        s = ttk.Style()
        s.configure('Horizontal.TScale', background='#ffffff')
        self.buy_scale_qty = tk.IntVar()
        self.sell_scale_qty = tk.IntVar()
        self.label_scale_buy = tk.Label(self.tool_bar, bg='#ffffff', text=0, textvariable=self.buy_scale_qty)
        self.label_scale_buy.place(x=10, y=y)
        self.label_scale_sell = tk.Label(self.tool_bar, bg='#ffffff', text=0, textvariable=self.sell_scale_qty)
        self.label_scale_sell.place(x=220, y=y)
        scale_buy = ttk.Scale(self.tool_bar, style='Horizontal.TScale', from_=0, to=100, command=self.on_buy_scale)
        scale_buy.place(x=60, y=y, width=140)
        scale_sell = ttk.Scale(self.tool_bar, style='Horizontal.TScale', from_=0, to=100, command=self.on_sell_scale)
        scale_sell.place(x=270, y=y, width=140)

        y += 30
        btn_buy = ttk.Button(self.tool_bar, text='BUY', command=self.hand_buy)
        btn_buy.place(x=10, y=y, width=190, height=25)
        btn_sell = ttk.Button(self.tool_bar, text='SELL', command=self.hand_sell)
        btn_sell.place(x=220, y=y, width=190, height=25)

    def on_buy_scale(self, val):
        v = int(float(val))
        self.buy_scale_qty.set(str(v) + '%')
        try:
            price = float(self.entry_buy_price.get())
            if price != '':
                qty = (float(self.entry_quote.get()) / price) * (v / 100)

                around_qty = self._bc.rules[self._bc.bot.pair]['around_qty']
                currency_quote = self._bc.bot.pair.split('_')[1].upper()

                if round(qty, around_qty) * price > self._bc.balances[currency_quote]['free']:
                    while round(qty, around_qty) * price > self._bc.balances[currency_quote]['free']:
                        qty -= 0.1 ** around_qty

                self.entry_buy_qty.delete(0, tk.END)
                self.entry_buy_qty.insert(0, self.ff(qty, around_qty))
        except Exception as e:
            self.log.post('* No buy scale error. ' + str(type(e).__name__) + ': ' + str(e))
            self.log.post('** Ошибка:\n' + traceback.format_exc())

    def on_sell_scale(self, val):
        v = int(float(val))
        self.sell_scale_qty.set(str(v) + '%')
        try:
            qty = float(self.entry_base.get()) * (v / 100)

            around_qty = self._bc.rules[self._bc.bot.pair]['around_qty']
            currency_base = self._bc.bot.pair.split('_')[0].upper()

            if round(qty, around_qty) > self._bc.balances[currency_base]['free']:
                while round(qty, around_qty) > self._bc.balances[currency_base]['free']:
                    qty -= 0.1 ** around_qty

            self.entry_sell_qty.delete(0, tk.END)
            self.entry_sell_qty.insert(0, self.ff(qty, around_qty))
        except Exception as e:
            self.log.post('* No sell scale error. ' + str(type(e).__name__) + ': ' + str(e))
            self.log.post('** Ошибка:\n' + traceback.format_exc())

    def hand_buy(self):
        order_price = float(self.entry_buy_price.get())
        order_qty = float(self.entry_buy_qty.get())
        if self._bc.check_trade_rules(order_price, order_qty):
            self._bc.send_order('buy', order_price, order_qty)

    def hand_sell(self):
        order_price = float(self.entry_buy_price.get())
        order_qty = float(self.entry_buy_qty.get())
        if self._bc.check_trade_rules(order_price, order_qty):
            self._bc.send_order('sell', order_price, order_qty)

    def _init_settings_window(self):
        # Функция показа окна настроек

        self.display_window = 'settings'
        self.tool_bar.forget()

        settings_names = self._bc.bot.get_item_names()
        strategy_names = self._bc.strategy.get_item_names()
        count_settings = len(settings_names) + len(strategy_names)

        self.full_height = count_settings * 25 + 150

        # Создаю внешний фрейм
        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        # Создаю холст во внешнем фрейме
        self.can = tk.Canvas(self.tool_bar, bd=0)
        self.can.config(width=self.width_root, height=self.height_root-20)
        self.can.config(scrollregion=(0, 2, 300, self.full_height))

        # Создаю скроллбар
        scroll_bar = ttk.Scrollbar(self.tool_bar, orient='vertical', command=self.can.yview, )
        self.can.config(yscrollcommand=scroll_bar.set)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.can.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        # Создаю внутренний фрейм
        inner_bar = tk.Frame(self.can, bd=0, bg='#ffffff', width=self.width_root, height=self.full_height + 5)
        self.can.create_window((0, 0), window=inner_bar, anchor=tk.NW)

        tk.Label(inner_bar, text='TRADES', bg='#ffffff', font='Arial 10 bold').place(x=10, y=5)

        y = 5
        tk.Label(inner_bar, bg='#ffffff', text='BOT SETTINGS', font='Arial 10 bold').place(x=10, y=y)

        for key in settings_names.keys():
            y += 25
            tk.Label(inner_bar, bg='#ffffff', text=settings_names[key]).place(x=10, y=y)
            if key == 'exchange':
                self.entry_bot_exchange = ttk.Combobox(inner_bar, values=[self._bc.exchanges])
                self.entry_bot_exchange.set(u'binance')
                self.entry_bot_exchange.place(x=150, y=y, width=240)
            else:
                exec(f'self.entry_bot_{key} = ttk.Entry(inner_bar)')
                exec(f'self.entry_bot_{key}.place(x=150, y=y, width=240)')

        y += 35
        tk.Label(inner_bar, bg='#ffffff', text='STRATEGY SETTINGS', font='Arial 10 bold').place(x=10, y=y)

        for key in strategy_names.keys():
            y += 25
            tk.Label(inner_bar, bg='#ffffff', text=strategy_names[key]).place(x=10, y=y)
            exec(f'self.entry_strategy_{key} = ttk.Entry(inner_bar)')
            exec(f'self.entry_strategy_{key}.place(x=150, y=y, width=240)')

        y += 50
        ttk.Button(inner_bar, text='Save', command=self.save_settings).place(x=150, y=y, width=120, height=30)

        self.view_settings()

        # Контроль колесика мыши
        # для Windows
        self._root.bind("<MouseWheel>", self.mouse_wheel)
        # для Linux
        self._root.bind("<Button-4>", self.mouse_wheel)
        self._root.bind("<Button-5>", self.mouse_wheel)

    def mouse_wheel(self, event):
        # воспроизведение события колесика мыши Linux or Windows
        if event.num == 5 or event.delta == -120:
            self.can.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            self.can.yview_scroll(-1, "units")

    @staticmethod
    def convert(value, value_type):

        if value_type is bool:
            return bool(value)
        elif value_type is int:
            return int(value)
        elif value_type is float:
            return float(value)
        elif value_type is str:
            return value
        elif value_type is list:
            return value.split(' ')
        return None

    def save_settings(self):

        settings_names = self._bc.bot.get_item_names()
        strategy_names = self._bc.strategy.get_item_names()

        settings_types = self._bc.bot.get_item_types()
        strategy_types = self._bc.strategy.get_item_types()

        for key in settings_names.keys():
            exec(f'self._bc.bot.{key} = self.convert(self.entry_bot_{key}.get(), settings_types[\'{key}\'])')

        for key in strategy_names.keys():
            exec(f'self._bc.strategy.{key} = '
                 f'self.convert(self.entry_strategy_{key}.get(), strategy_types[\'{key}\'])')

        self._bc.bot.save()
        self._bc.strategy.save()

    def view_settings(self):

        settings_names = self._bc.bot.get_item_names()
        strategy_names = self._bc.strategy.get_item_names()

        for key in settings_names.keys():
            exec(f'self.entry_bot_{key}.delete(0, tk.END)')
            exec(f'self.entry_bot_{key}.insert(0, self._bc.bot.{key})')

        for key in strategy_names.keys():
            exec(f'self.entry_strategy_{key}.delete(0, tk.END)')
            exec(f'self.entry_strategy_{key}.insert(0, self._bc.strategy.cur.{key})')
