import random
import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
from db import load_balances, save_balances

# Загрузка данных о балансе пользователей
user_coins = load_balances()
used_promo_codes = {}  # Новый словарь для отслеживания использованных промокодов

# Промокоды и соответствующие бонусы
promo_codes = {
    "terabytelove": 1000  # Пример промокода, который дает 1000 монет
}


# Команда для ввода промокодов
@commands.command(name="promo")
async def promo(ctx, code: str):
    user_id = str(ctx.author.id)

    # Удаляем сообщение пользователя, чтобы оно не было видно другим
    await ctx.message.delete()

    # Проверка, использовал ли пользователь промокод
    if user_id in used_promo_codes:
        embed = discord.Embed(
            title="Ошибка!",
            description=f"{ctx.author.name}, вы уже использовали промокод!",
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
        return

    # Проверка на существование промокода
    if code in promo_codes:
        bonus = promo_codes[code]

        # Начисляем бонусные монеты пользователю
        if user_id in user_coins:
            user_coins[user_id] += bonus
        else:
            user_coins[user_id] = bonus

        # Сохраняем обновленные данные в файл
        save_balances(user_coins)

        # Помечаем, что пользователь использовал промокод
        used_promo_codes[user_id] = code

        # Создаем Embed-сообщение с успешным бонусом
        embed = discord.Embed(
            title="Поздравляем!",
            description=f"{ctx.author.name}, вы получили {bonus} монет!",
            color=discord.Color.from_rgb(23, 23, 23)
        )
        embed.set_footer(text="Спасибо за использование промокода!")
        await ctx.send(embed=embed)
    else:
        # Создаем Embed-сообщение с ошибкой, если промокод неверный
        embed = discord.Embed(
            title="Ошибка!",
            description=f"Ошибка, вы ввели неверный промокод.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


# Команда для получения монет
@commands.command(name="coin")
@commands.cooldown(1, 10, commands.BucketType.user)
async def coin(ctx):
    user_id = str(ctx.author.id)
    coins = random.randint(1, 5)

    # Добавляем монеты пользователю
    if user_id in user_coins:
        user_coins[user_id] += coins
    else:
        user_coins[user_id] = coins

    # Сохраняем обновленные данные
    save_balances(user_coins)

    # Создание Embed-сообщения
    embed = discord.Embed(
        title=f"{ctx.author.name}, вы получили монеты!",
        description=f"Вы получили {coins} монет. Поздравляем!",
        color=discord.Color.from_rgb(23, 23, 23)
    )
    embed.set_footer(text="Наслаждайтесь игрой!")  # Можно добавить дополнительный текст внизу

    # Отправляем Embed-сообщение в канал
    await ctx.message.reply(embed=embed)


# Команда для проверки баланса
@commands.command(name="balance")
async def balance(ctx):
    user_id = str(ctx.author.id)

    # Если у пользователя есть монеты, показываем баланс, иначе 0 монет
    balance = user_coins.get(user_id, 0)

    banner_url = "https://cdn.discordapp.com/attachments/1294373911806476340/1305295232321192007/GLOBAL_SERVER.png?ex=6732826a&is=673130ea&hm=1a8df0b7f58016ad0f4f26d8cda0d7142c811d2dfbf681e30c6e687ff3c195b2&"

    # Создание Embed-сообщения для отображения баланса
    embed = discord.Embed(
        title=f"{ctx.author.name} Ваш текущий баланс: {balance} монет.",
        color=discord.Color.from_rgb(23, 23, 23)
    )

    embed.set_image(url=banner_url)
    embed.set_thumbnail(url=ctx.author.avatar.url)  # Аватар пользователя

    # Отправляем Embed-сообщение с балансом
    await ctx.message.reply(embed=embed)


# Обработка ошибки, если пользователь превысил лимит команд
@coin.error
async def coin_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f"Пожалуйста, подождите {error.retry_after:.2f} секунд до следующего использования команды.")
