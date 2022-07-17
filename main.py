# Торговый бот с открытым исходным кодом.
# Программа написана с максимально возможной автоматизацией проекта

# Funnymay Open Bot
# contacts: Kirill Savin
# telegram: @savinkirillnick

from settings import BotSettings
from positions import Position
from logs import Logs

# создаем объект настроек бота
bs = BotSettings({})
# создаем объект позиции
pos = Position({})
# создаем объект лог
log = Logs()
