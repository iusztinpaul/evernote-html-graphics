from typing import List

from data_types import MoneyDistributionState, MoneyDistribution, MoneyDistributionTitle, Currency
from validators import TitleValidator, KeyValidator, ValueValidator, CurrencyValidator


class HTMLMoneyDistributionParser:
    title_validator = TitleValidator
    key_validator = KeyValidator
    value_validator = ValueValidator
    currency_validator = CurrencyValidator

    def __init__(self, data: List[str]):
        self._data = data
        self._data_index = 0

        self._current_state = MoneyDistributionState.TITLE
        self._current_title = None
        self._current_key = None
        self._money_distribution = MoneyDistribution()

    @property
    def money_distribution(self):
        return self._money_distribution

    def parse(self):
        while self._data_index < len(self._data):
            item = self._data[self._data_index]
            self._current_state = self._get_next(item)

    def _get_next(self, item: str):
        next_move = {
            MoneyDistributionState.TITLE: self._get_next_title,
            MoneyDistributionState.KEY: self._get_next_key,
            MoneyDistributionState.VALUE: self._get_next_value,
            MoneyDistributionState.CURRENCY: self._get_next_currency
        }[self._current_state]

        return next_move(item)

    def _get_next_title(self, item: str) -> MoneyDistributionState:
        if self.title_validator.is_valid(item):
            normalized_title = self.title_validator.normalize(item)

            self._current_title = MoneyDistributionTitle[normalized_title]
            self.money_distribution.add_title(self._current_title)

            return self._next(MoneyDistributionState.KEY)

        return self._next(MoneyDistributionState.TITLE)

    def _get_next_key(self, item: str) -> MoneyDistributionState:
        if self.key_validator.is_valid(item):
            self._money_distribution.add_key(self._current_title, item)
            self._current_key = item

            return self._next(MoneyDistributionState.VALUE)

        return self._next(MoneyDistributionState.KEY)

    def _get_next_value(self, item: str) -> MoneyDistributionState:
        if self.value_validator.is_valid(item):
            self._money_distribution.add_value(self._current_title, self._current_key, item)

            return self._next(MoneyDistributionState.CURRENCY)

        return self._next(MoneyDistributionState.VALUE)

    def _get_next_currency(self, item: str) -> MoneyDistributionState:
        if self.currency_validator.is_valid(item):
            item = self.currency_validator.normalize(item)
            item = Currency[item]
            self.money_distribution.add_currency(self._current_title, self._current_key, item)

            if self.title_validator.is_title_paragraph_finished(self._current_key):
                return self._next(MoneyDistributionState.TITLE)
            else:
                return self._next(MoneyDistributionState.KEY)

        return self._next(MoneyDistributionState.CURRENCY)

    def _next(self, next_state):
        assert next_state is not None

        self._data_index += 1

        return next_state
