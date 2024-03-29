"""Торговый бот с открытым исходным кодом: OpenBot.
Программа написана с максимально возможной автоматизацией проекта.

Funnymay Open Bot
contacts: Kirill Savin
telegram: @savinkirillnick

"""

import tkinter as tk
from gui import MainWindow
from threading import Thread
import ccxt
from controller import BotController


__version__ = 'ver. dev'


def _on_key_release(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

    if event.keycode == 65 and ctrl and event.keysym.lower() != "a":
        event.widget.event_generate("<<SelectAll>>")


if __name__ == '__main__':

    # Создаем объект состояния бота
    bc = BotController()
    bc.exchanges = ccxt.exchanges

    # Создаем объект API, в зависимости, какая биржа у нас подключена
    api = None
    try:
        # Получаем список наобходимых данных
        required = eval(f'ccxt.{bc.bot.exchange}.requiredCredentials')

        # Удаляем apiKey и secret, оставляем дополнительные параметры
        del required['apiKey']
        del required['secret']

        # Формируем словарь аргументов
        args = {'apiKey': bc.bot.api_key, 'secret': bc.bot.api_secret}
        args.update({key: bc.bot.api_optional for key in required})

        # запускаем инициализацию api
        api = eval(f'ccxt.{bc.bot.exchange}({args})')
    except Exception as e:
        print(e.args)
        quit()

    # Если апи инициализировалось, то анациализируем настройки биржи
    if api is not None:
        bc.api = api
        bc.init_api()

    # Запускаем потоки и садим функции обновления информации на каждый поток
    Thread(target=bc.update_prices, daemon=True).start()
    Thread(target=bc.update_strategies, daemon=True).start()
    Thread(target=bc.update_order, daemon=True).start()
    Thread(target=bc.update_depth, daemon=True).start()
    Thread(target=bc.update_activity, daemon=True).start()

    # Создаем корневой объект ткинтер
    root = tk.Tk()
    app = MainWindow(root, bc)

    # Вычисляем расширение экрана пользователя и задаем размеры окна программы
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app_width = 420
    app_height = 480

    root.title('Open Bot ' + __version__)
    root.geometry(f'{app_width}x{app_height}+{screen_width//2-app_width//2}+{screen_height//2-app_height//2}')
    root.minsize(app_width, app_height)
    root.bind_all("<Key>", _on_key_release, "+")
    root.resizable(False, False)
    root.mainloop()
