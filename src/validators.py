import re

import data_types


class Validator:
    @classmethod
    def is_valid(cls, item: str) -> bool:
        raise NotImplementedError()


class PatternValidator(Validator):
    PATTERN = None

    @classmethod
    def is_valid(cls, item: str) -> bool:
        assert cls.PATTERN is not None

        item = item.strip()

        return bool(cls.PATTERN.match(item))


class HardcodedValidator(Validator):
    ITEMS = None

    @classmethod
    def normalize(cls, data: str) -> str:
        assert cls.ITEMS is not None

        data = data.upper()

        for item in cls.ITEMS:
            if item in data:
                return item

        return ''

    @classmethod
    def is_valid(cls, item: str) -> bool:
        return bool(cls.normalize(item))


class KeyValidator(PatternValidator):
    """
    A key / name should contain only alphabet letters and &.
    """

    PATTERN = re.compile(r'^[a-zA-Z&]+$')

    BANNED_KEYWORDS = [currency.value for currency in data_types.Currency]

    @classmethod
    def is_valid(cls, item: str) -> bool:
        item = item.strip().upper()

        if item in cls.BANNED_KEYWORDS:
            return False

        return super().is_valid(item)


class ValueValidator(PatternValidator):
    """
        A value should contain only digits.
    """

    PATTERN = re.compile(r'^[0-9]+[.,]?[0-9]*$')


class TitleValidator(HardcodedValidator):
    """
        A title should be part of the ITEMS tuple of strings.
    """

    ITEMS = [title.value for title in data_types.MoneyDistributionTitle]

    FINISH_KEYWORD = 'TOTAL'

    @classmethod
    def is_title_paragraph_finished(cls, key):
        key = key.upper()

        return cls.FINISH_KEYWORD in key


class CurrencyValidator(HardcodedValidator):
    """
        A currency should be part of the ITEMS tuple of strings.
    """

    ITEMS = [currency.value for currency in data_types.Currency]
