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
from state import BotState


__version__ = 'ver. dev'


if __name__ == '__main__':

    # Создаем объект состояния бота
    bs = BotState()
    bs.exchanges = ccxt.exchanges

    # Создаем объект API, в зависимости, какая биржа у нас подключена
    api = None
    try:
        # Получаем список наобходимых данных
        required = eval(f'ccxt.{bs.bot.exchange}.requiredCredentials')

        # Удаляем apiKey и secret, оставляем дополнительные параметры
        del required['apiKey']
        del required['secret']

        # Формируем словарь аргументов
        args = {'apiKey': bs.bot.api_key, 'secret': bs.bot.api_secret}
        args.update({key: bs.bot.api_optional for key in required})

        # запускаем инициализацию api
        api = eval(f'ccxt.{bs.bot.exchange}({args})')
    except Exception as e:
        print(e.args)
        quit()

    # Если апи инициализировалось, то анациализируем настройки биржи
    if api is not None:
        bs.api = api
        bs.init_api()

    # Запускаем потоки и садим функции обновления информации на каждый поток
    Thread(target=bs.update_prices, daemon=True).start()
    Thread(target=bs.update_strategies, daemon=True).start()
    Thread(target=bs.update_order, daemon=True).start()
    Thread(target=bs.update_depth, daemon=True).start()
    Thread(target=bs.update_activity, daemon=True).start()

    # Создаем корневой объект ткинтер
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
