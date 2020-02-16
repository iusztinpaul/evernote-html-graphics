import matplotlib.pyplot as plt

from data_types import MoneyDistribution


class MoneyDistributionPieChart:
    def __init__(self, money_distribution: MoneyDistribution):
        self._money_distribution = money_distribution

    def plot(self):
        fig, axs = plt.subplots(nrows=3, ncols=2)

        total_income, total_currency, income_titles, income_distribution = self._money_distribution.income_distribution

        axs[0][0].set_title(f'Income: {total_income} {total_currency}', weight='bold', size=14)
        axs[0][0].pie(income_distribution, labels=income_titles, autopct='%2.2f%%')
        axs[0][0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        total_income, total_currency, spending_titles, spending_distribution, spending_sub_distributions = self._money_distribution.spending_distribution

        axs[1][0].set_title(f'Spending: {total_income} {total_currency}', weight='bold', size=14)
        axs[1][0].pie(spending_distribution, labels=spending_titles, autopct='%2.2f%%')
        axs[1][0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        for index, spending in enumerate(spending_sub_distributions):
            main_title, total, currency, spending_sub_titles, distribution = spending

            col = 0
            row = 2

            if index > 0:
                col = 1
                row = index - 1

            axs[row][col].set_title(f'{main_title}: {total} {currency}', weight='bold', size=14)
            axs[row][col].pie(distribution, labels=spending_sub_titles, autopct='%2.2f%%')
            axs[row][col].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()
