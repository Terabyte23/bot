import discord
from discord.ext import commands
from discord.ui import Button, View

# Настройка бота
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)


# Команда / для вывода доступных команд
@bot.command()
async def help(ctx):
    # Создаем кнопки для каждой команды
    button1 = Button(label="Баланс", style=discord.ButtonStyle.green, custom_id="balance")
    button2 = Button(label="Монеты", style=discord.ButtonStyle.blurple, custom_id="coin")

    # Создаем объект View для добавления кнопок
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    # Отправляем сообщение с кнопками
    await ctx.send("Нажмите на кнопку, чтобы использовать команду!", view=view)


# Обработчик для кнопки "Баланс"
@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == 'balance':
            # Здесь код для обработки команды баланса
            await interaction.response.send_message("Ваш баланс: 100 монет.")  # Пример ответа
        elif interaction.data['custom_id'] == 'coin':
            # Здесь код для обработки команды монет
            await interaction.response.send_message("Вы получили 5 монет!")  # Пример ответа


# Запуск бота
bot.run('MTMwNTI3MzI2NTg5NTM3ODk1NA.Gv6ZJc.RZlcu9B28b4wfxegt3o9rCMAJi6j2P26JAwbwg')
