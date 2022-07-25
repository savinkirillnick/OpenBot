# Класс графического интерфейса

import tkinter as tk


# Список разделов программы
from time import sleep

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

        self.__root = root
        self.__bot_state = bot_state
        self.display_window = 'main'
        self.logs_journal = ['Welcome to Open Bot', ]

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
        self.logs_box.insert(tk.END, '\n'.join(self.logs_journal)+'\n' if not message else message+'\n')
        self.logs_box.configure(state='disable')
        self.logs_box.yview_moveto(1)

    def insert_logs(self, message):
        self.logs_journal.append(message)
        self._show_logs(message)

    def _init_depth_window(self):
        pass

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
