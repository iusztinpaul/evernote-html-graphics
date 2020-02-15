import matplotlib.pyplot as plt

from data_types import MoneyDistribution


class MoneyDistributionPieChart:
    def __init__(self, money_distribution: MoneyDistribution):
        self._money_distribution = money_distribution

    def plot(self):
        fig, axs = plt.subplots(2)

        income_titles = self._money_distribution.income_titles
        total_income, total_currency, income_distribution = self._money_distribution.income_distribution

        axs[0].set_title(f'Income: {total_income} {total_currency}', weight='bold', size=18)
        axs[0].pie(income_distribution, labels=income_titles, autopct='%2.2f%%')
        axs[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        spending_titles = self._money_distribution.spending_titles
        total_income, total_currency, spending_distribution = self._money_distribution.spending_distribution

        axs[1].set_title(f'Spending: {total_income} {total_currency}', weight='bold', size=18)
        axs[1].pie(spending_distribution, labels=spending_titles, autopct='%2.2f%%')
        axs[1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
