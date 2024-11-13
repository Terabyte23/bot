import discord
from discord.ext import commands
from commands import coin, balance, promo  # Импортируем команды из файла commands

# Укажите ваш токен
TOKEN = ''

# Включаем нужные intents
intents = discord.Intents.default()
intents.message_content = True  # Разрешаем боту видеть содержимое сообщений

# Указываем префикс команд и intents для бота
bot = commands.Bot(command_prefix='/', intents=intents)

# Регистрируем команды
bot.add_command(coin)
bot.add_command(balance)
bot.add_command(promo)

# Событие, когда бот готов к работе
@bot.event
async def on_ready():
    print(f'Бот {bot.user} подключен и готов к работе!')

# Запуск бота
bot.run(TOKEN)
