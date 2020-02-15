from enum import Enum
from typing import Set


class MoneyDistributionState(Enum):
    TITLE = 'TITLE'
    KEY = 'KEY'
    VALUE = 'VALUE'
    CURRENCY = 'CURRENCY'


class MoneyDistributionTitle(Enum):
    INVESTMENTS = 'INVESTMENTS'
    INVESTMENT = 'INVESTMENT'
    NEEDS = 'NEEDS'
    NEED = 'NEED'
    WANTS = 'WANTS'
    WANT = 'WANT'
    INCOME = 'INCOME'

    def __str__(self):
        return str(self.value)


class Currency(Enum):
    RON = 'RON'
    EUR = 'EUR'
    USD = 'USD'


class MoneyDistribution:
    def __init__(self):
        self._money_distribution = {}

    @property
    def spending_titles(self) -> Set[MoneyDistributionTitle]:
        titles = self._money_distribution.keys()
        titles = {MoneyDistributionTitle[title] for title in titles}
        titles = titles - {MoneyDistributionTitle.INCOME}

        return titles

    @property
    def spending_distribution(self):
        assert MoneyDistributionTitle.INCOME.value in self._money_distribution

        total_income = self.get_total_value(MoneyDistributionTitle.INCOME)
        total_currency = self.get_total_currency(MoneyDistributionTitle.INCOME)

        sub_totals = []
        for title in self.spending_titles:
            if title != MoneyDistributionTitle.INCOME:
                total_value = self.get_total_value(title)
                sub_totals.append(total_value)

        return total_income, total_currency, [
            sub_total * 100 / total_income
            for sub_total in sub_totals
        ]

    @property
    def income_titles(self):
        return self.get_title(MoneyDistributionTitle.INCOME).keys() - {'TOTAL'}

    @property
    def income_distribution(self):
        assert MoneyDistributionTitle.INCOME.value in self._money_distribution

        total_income = self.get_total_value(MoneyDistributionTitle.INCOME)
        total_currency = self.get_total_currency(MoneyDistributionTitle.INCOME)

        sub_income_keys = self.get_title(MoneyDistributionTitle.INCOME).keys()
        sub_income_values = [
           self.get_value(MoneyDistributionTitle.INCOME, sub_income_key)
           for sub_income_key in sub_income_keys
           if sub_income_key != 'TOTAL'
        ]

        return total_income, total_currency, [
            sub_income * 100 / total_income
            for sub_income in sub_income_values
        ]

    def get_title(self, title: MoneyDistributionTitle):
        return self._money_distribution[title.value]

    def get_value(self, title: MoneyDistributionTitle, key: str):
        return self._money_distribution[title.value][key]['value']

    def get_currency(self, title: MoneyDistributionTitle, key: str):
        return self._money_distribution[title.value][key]['currency']

    def get_total_value(self, title: MoneyDistributionTitle):
        return self.get_value(title, 'TOTAL')

    def get_total_currency(self, title: MoneyDistributionTitle):
        return self.get_currency(title, 'TOTAL')

    def add_title(self, title: MoneyDistributionTitle):
        self._money_distribution[title.value] = dict()

    def add_key(self, title: MoneyDistributionTitle, key: str):
        self._money_distribution[title.value][key] = {
            'value': None,
            'currency': None
        }

    def add_value(self, title: MoneyDistributionTitle, key: str, value: str):
        self._money_distribution[title.value][key]['value'] = float(value)

    def add_currency(self, title: MoneyDistributionTitle, key: str, currency: Currency):
        self._money_distribution[title.value][key]['currency'] = currency.value
