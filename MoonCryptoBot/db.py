import json

BALANCE_FILE = 'balances.json'

# Загрузка балансов из файла
def load_balances():
    try:
        with open(BALANCE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Если файл не найден, возвращаем пустой словарь

# Сохранение балансов в файл
def save_balances(balances):
    with open(BALANCE_FILE, 'w') as f:
        json.dump(balances, f)
