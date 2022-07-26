# Класс графического интерфейса

import tkinter as tk
from tkinter import ttk


# Список разделов программы
gui_menu = ['main',
            'depth',
            'orders',
            'trades',
            'terminal',
            'position',
            'settings'
            ]


class MainWindow(tk.Frame):

    def __init__(self, root, bot_state):
        super().__init__(root)

        self._root = root
        self._bot_state = bot_state
        self.display_window = 'main'

        self.width_root = 420
        self.height_root = 480

        self._init_menu()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

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
        self.logs_box.configure(state='normal')
        self.logs_box.insert(tk.END, '\n'.join(self._bot_state.log.logs_journal)+'\n' if not message else message+'\n')
        self.logs_box.configure(state='disable')
        self.logs_box.yview_moveto(1)

    def insert_logs(self, message):
        self._bot_state.log.post(message)
        self._show_logs(message)

    def _init_depth_window(self):

        self.display_window = 'depth'
        self.tool_bar.forget()

        self.tool_bar = tk.Frame(bg='#ffffff', bd=0, width=self.width_root, height=self.height_root-20)
        self.tool_bar.pack(side=tk.TOP, fill=tk.BOTH)

        tk.Label(self.tool_bar, text='Bid', bg='#ffffff', font='Arial 10 bold').place(x=10, y=10)
        tk.Label(self.tool_bar, text='Ask', bg='#ffffff', font='Arial 10 bold').place(x=210, y=10)

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ('bid_price', 'bid_qty', 'bid_sum', 'ask_price', 'ask_qty', 'ask_sum',)
        self.tree.column('#0', width=0, minwidth=0, stretch=tk.NO)
        self.tree.column('bid_price', width=70, minwidth=70, stretch=tk.NO)
        self.tree.column('bid_qty', width=70, minwidth=70, stretch=tk.NO)
        self.tree.column('bid_sum', width=70, minwidth=70, stretch=tk.NO)
        self.tree.column('ask_price', width=70, minwidth=70, stretch=tk.NO)
        self.tree.column('ask_qty', width=70, minwidth=70, stretch=tk.NO)
        self.tree.column('ask_sum', width=70, minwidth=70, stretch=tk.NO)

        self.tree.heading('bid_price', text='Price', anchor=tk.W)
        self.tree.heading('bid_qty', text='Qty', anchor=tk.W)
        self.tree.heading('bid_sum', text='Sum', anchor=tk.W)
        self.tree.heading('ask_price', text='Price', anchor=tk.W)
        self.tree.heading('ask_qty', text='Qty', anchor=tk.W)
        self.tree.heading('ask_sum', text='Sum', anchor=tk.W)

        around_price = self._bot_state.rules[self._bot_state.bot.pair]['around_price']
        around_qty = self._bot_state.rules[self._bot_state.bot.pair]['around_qty']

        for i in range(max(len(self._bot_state.depth['bids']), len(self._bot_state.depth['asks']))):
            if len(self._bot_state.depth['bids']) > i and len(self._bot_state.depth['asks']) > i:
                self.tree.insert('', 'end', 'depth_' + str(i), values=(
                    0.0 if not self._bot_state.depth['bids'][i][0]
                    else f"{self._bot_state.depth['bids'][i][0]}:.{around_price}f",
                    0.0 if not self._bot_state.depth['bids'][i][1]
                    else f"{self._bot_state.depth['bids'][i][1]}:.{around_qty}f",
                    0.0 if not self._bot_state.depth['bids'][i][0]
                    else f"{(self._bot_state.depth['bids'][i][0] * self._bot_state.depth['bids'][i][1])} \
                    :.{around_price}f",
                    0.0 if not self._bot_state.depth['asks'][i][0]
                    else f"{self._bot_state.depth['asks'][i][0]}:.{around_price}f",
                    0.0 if not self._bot_state.depth['asks'][i][1]
                    else f"{self._bot_state.depth['asks'][i][1]}:.{around_qty}f",
                    0.0 if not self._bot_state.depth['asks'][i][0]
                    else f"{(self._bot_state.depth['asks'][i][0] * self._bot_state.depth['asks'][i][1])} \
                    :.{around_price}f",
                ))
            else:
                self.tree.insert('', 'end', 'depth_' + str(i), values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

        self.tree.pack(fill=tk.X)

    def _init_orders_window(self):
        pass

    def _init_trades_window(self):
        pass

    def _init_terminal_window(self):
        pass

    def _init_position_window(self):
        pass

    def _init_settings_window(self):
        pass
