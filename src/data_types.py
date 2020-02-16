from enum import Enum
from typing import Set, List, Tuple, Any


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

    def spending_sub_titles(self, title: MoneyDistributionTitle) -> Set[str]:
        return self._money_distribution[title.value].keys() - {'TOTAL'}

    @property
    def spending_distribution(self):
        assert MoneyDistributionTitle.INCOME.value in self._money_distribution

        total_income = self.get_total_value(MoneyDistributionTitle.INCOME)
        total_currency = self.get_total_currency(MoneyDistributionTitle.INCOME)

        sub_totals_titles = []
        sub_totals = []
        spending_sub_distributions = []

        for title in self.spending_titles:
            if title != MoneyDistributionTitle.INCOME:
                sub_totals_titles.append(title)
                total_value = self.get_total_value(title)
                sub_totals.append(total_value)

                spending_sub_distribution = self.spending_sub_distribution(title)
                spending_sub_distributions.append(spending_sub_distribution)

        return total_income, total_currency, sub_totals_titles, [
            sub_total * 100 / total_income
            for sub_total in sub_totals
        ], spending_sub_distributions

    def spending_sub_distribution(self, title: MoneyDistributionTitle):
        sub_titles_data = self._money_distribution[title.value].copy()

        if not self._check_unicity_for_currency(sub_titles_data):
            return Exception('Cannot compute graphic: Distribution of different currencies for title: {}'.format(title))

        total_value = sub_titles_data['TOTAL']['value']
        total_currency = sub_titles_data['TOTAL']['currency']
        del sub_titles_data['TOTAL']

        sub_title_keys = []
        sub_title_values = []
        for sub_title_key, sub_title_cost in sub_titles_data.items():
            sub_title_keys.append(sub_title_key)

            sub_title_value = sub_title_cost['value']
            sub_title_values.append(sub_title_value)

        return title, total_value, total_currency, sub_title_keys, [
            sub_title_value * 100 / total_value
            for sub_title_value in sub_title_values
        ]

    def _check_unicity_for_currency(self, sub_titles_data: dict):
        if len(sub_titles_data) == 0:
            return True

        sub_titles_currency = [sub_title_data['currency'] for sub_title_data in sub_titles_data.values()]
        example_currency = sub_titles_currency.pop(0)

        for currency in sub_titles_currency:
            if example_currency != currency:
                return False

        return True

    @property
    def income_titles(self):
        return self.get_title(MoneyDistributionTitle.INCOME).keys() - {'TOTAL'}

    @property
    def income_distribution(self):
        assert MoneyDistributionTitle.INCOME.value in self._money_distribution

        total_income = self.get_total_value(MoneyDistributionTitle.INCOME)
        total_currency = self.get_total_currency(MoneyDistributionTitle.INCOME)

        sub_income_keys = list(self.get_title(MoneyDistributionTitle.INCOME).keys() - {'TOTAL'})
        sub_income_values = [
           self.get_value(MoneyDistributionTitle.INCOME, sub_income_key)
           for sub_income_key in sub_income_keys
        ]

        return total_income, total_currency, sub_income_keys, [
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
