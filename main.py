"""Торговый бот с открытым исходным кодом: OpenBot.
Программа написана с максимально возможной автоматизацией проекта.

Funnymay Open Bot
contacts: Kirill Savin
telegram: @savinkirillnick

"""
import ccxt

from settings import BotSettings
from position import Position
from logs import Logs
from strategy import Sniper


if __name__ == '__main__':
    # создаем объект настроек бота
    bs = BotSettings()
    # создаем объект позиции
    pos = Position()
    # создаем объект лог
    log = Logs()


