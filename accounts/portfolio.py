
from functools import reduce

from .asset import Asset
from .debt import Debt

class Portfolio:

    def __init__(self, accounts=[]):
        self.assets = list(filter(lambda x: isinstance(x, Asset), accounts))
        self.debts = list(filter(lambda x: isinstance(x, Debt), accounts))
        self.lookup = dict()
        for a in accounts:
            self.lookup[a.name] = a

    def add_account(self, acc):
        self.accounts.append(acc)

    @property
    def asset_total(self):
        return reduce(lambda a, b: float(a) + float(b), self.assets, 0)

    @property
    def debt_total(self):
        return reduce(lambda a, b: float(a) + float(b), self.debts, 0)

    @property
    def balance(self):
        return self.asset_total - self.debt_total

    @balance.setter
    def balance(self, value):
        assert False, 'Cannot set balance of a portfolio.'

    def __str__(self):
        return f'Assets: {self.asset_total:.2f}\t' \
            f'Debts: {self.debt_total:.2f}\t' \
            f'Total: {self.balance:.2f}'

    def printall():
        for a in (*self.assets, *self.debts):
            print(a)

    def step(self):
        for i, acc in enumerate(self.assets):
            self.assets[i].step_month()

        for i, acc in enumerate(self.debts):
            self.debts[i].step_month()
