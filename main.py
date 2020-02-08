import click
import re
import sys
import os
import math
from collections import namedtuple
import functools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Account:

    def __init__(self, principle, monthly, rate=0, name=None):
        self.balance = principle
        self.principle = principle
        self.monthly = monthly
        self.rate = rate
        self.name = name

    def step_month(self):
        self.balance += self.balance * rate

    def interest(self):
        return balance - principle

    def __str__(self):
        if self.name is None:
            return f'{type(self).__name__}: {self.balance}'
        else:
            return f'{self.name} ({type(self).__name__}): {self.balance}'

    def __float__(self):
        return float(self.balance)

class PNNL401K(Account):

    def __init__(self, principle, rate, monthly):
        pass

class MoneyMarket(Account):
    Rate = namedtuple('Range', ['range', 'rate'])
    rates = [
            Rate((0, 2499.99),          0.0000),
            Rate((2500, 4999.99),       0.0020),
            Rate((5000, 14999.99),      0.0025),
            Rate((15000, 24999.99),     0.0030),
            Rate((25000, 49999.99),     0.0040),
            Rate((50000, 99999.99),     0.0050),
            Rate((100000, 999999),      0.0055),
            ]

    def __init__(self, principle, monthly):
        for i in rates:
            if i.range[0] <= principle <= i.range[1]:
                rate = i.rate
        super().__init__(principle, rate, monthly)

class CertificateAccount(Account):
    rates = {
            6: .0075,
            12: .0149,
            18: .0164,
            24: .0174,
            30: .0184,
            36: .0189,
            48: .0194,
            60: .0199,
            }

    def __init__(self, principle, months, name=None):
        assert months in rates.keys(), 'Number of months must be valid.'
        rate = rates[months]
        super().__init__(principle, rate, monthly=0, name=name)

class Loan(Account):

    def __init__(self, principle, rate, monthly):
        super().__init__(principle, rate, monthly)

    def step_month(self, additional_payment=0):
        self.balance -= ( self.monthly + additional_payment )
        self.balance += ( self.principle * self.rate )

@click.command()
@click.option('-m', '--months', type=int, default=12, help='Number of months to simulate')
def main(months):
    accounts = [
            Loan(2750, rate=0.0505,     monthly=0),
            Loan(1073, rate=0.0505,     monthly=0),
            Loan(4500, rate=0.0445,     monthly=0),
            Loan(2200, rate=0.0445,     monthly=0),
            Loan(3500, rate=0.0376,     monthly=0),
            Loan(2243, rate=0.0367,     monthly=0),
            ]

    print('\nTotal: ', functools.reduce(lambda a, b: float(a) + float(b), accounts))

    for month in range(months):
        for i, acc in enumerate(accounts):
            print(acc)
            accounts[i].step_month()

        print('\nTotal: ', functools.reduce(lambda a, b: float(a) + float(b), accounts))

if __name__ == '__main__':
    main()

