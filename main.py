"""Торговый бот с открытым исходным кодом: OpenBot.
Программа написана с максимально возможной автоматизацией проекта.

Funnymay Open Bot
contacts: Kirill Savin
telegram: @savinkirillnick

"""

from settings import BotSettings
from position import Position
from logs import Logs
from strategy import Sniper

# создаем объект настроек бота
bs = BotSettings()
# создаем объект позиции
pos = Position()
# создаем объект лог
log = Logs()


