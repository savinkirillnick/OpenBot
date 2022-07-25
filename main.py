"""Торговый бот с открытым исходным кодом: OpenBot.
Программа написана с максимально возможной автоматизацией проекта.

Funnymay Open Bot
contacts: Kirill Savin
telegram: @savinkirillnick

"""

import tkinter as tk
from gui import MainWindow
import ccxt

from state import BotState


__version__ = 'ver. dev'


if __name__ == '__main__':

    # Создаем объект состояния бота
    bs = BotState()

    root = tk.Tk()
    app = MainWindow(root, bs)

    # Вычисляем расширение экрана пользователя и задаем размеры окна программы
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 420
    app_height = 480

    root.title('Open Bot ' + __version__)
    root.geometry(f'{app_width}x{app_height}+{screen_width//2-app_width//2}+{screen_height//2-app_height//2}')
    root.minsize(app_width, app_height)
    root.resizable(False, False)
    root.mainloop()
