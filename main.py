import datetime as dt

# Отсутствует docstring для класса Record.
# Рекомендуется использовать type hints для параметров.
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Нечитаемый перенос. Лучше явно проверить date is None и использовать if-else.
        # Использование пустой строки как default может привести к ложному срабатыванию,
        # если пользователь передаст date='' намеренно. Лучше date=None.
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    # Нет docstring для класса.
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменная цикла Record затеняет имя класса. Следует использовать record (строчными).
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount  # Лучше использовать +=
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Дважды вычисляется разница в днях. Можно сохранить в переменную.
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Нет docstring.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Использован бэкслеш для переноса строки, что запрещено требованиями.
            # Вместо этого используйте круглые скобки или многострочную f-строку.
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Лишние скобки вокруг строки. else необязателен, т.к. после if уже return.
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Избыточное преобразование в float. Достаточно USD_RATE = 60.0 или просто 60.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Параметры USD_RATE и EURO_RATE по умолчанию избыточны. Внутри метода можно обращаться к self.USD_RATE.
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        # Непоследовательность: выше использовалось currency, здесь currency_type.
        # Лучше везде использовать currency.
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # ОШИБКА! Использовано сравнение (==) вместо присваивания (=).
            # Строка cash_remained == 1.00 ничего не меняет. Для рубля не нужно менять cash_remained.
            # Просто уберите эту строку.
            cash_remained == 1.00
            currency_type = 'руб'
        # Нет обработки случая, если передана неподдерживаемая валюта. Следует raise ValueError.
        if cash_remained > 0:
            # Для рубля округление через round, для долга через format – лучше единообразие.
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Конкатенация строк через пробел неочевидна. Лучше использовать f-строку.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Этот метод не нужен, т.к. родительский уже реализует get_week_stats.
    # Более того, переопределение без возврата значения ломает функциональность:
    # вызов cash_calculator.get_week_stats() вернёт None вместо суммы.
    # Удалите этот метод.
    def get_week_stats(self):
        super().get_week_stats()
