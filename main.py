import click
import re
import sys
import os
import math
import functools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from accounts import Debt, Asset, Portfolio, Loan

@click.command()
@click.option('-m', '--months', type=int, default=12, help='Number of months to simulate')
def main(months):
    portfolio = Portfolio([
            # Personal federal loans
            Loan(2750, monthly=0, APY=0.0505, name='DS18'),
            # Loan(1073, monthly=0, APY=0.0505, name='DU18'),
            Loan(4500, monthly=0, APY=0.0445, name='DS17'),
            # Loan(2200, monthly=0, APY=0.0445, name='DU17'),
            Loan(3500, monthly=0,   APY=0.0376, name='DS16'),
            Loan(2243, monthly=20,  APY=0.0367, name='DU16'),

            # Private parent plus loans
            Loan(21801.79, monthly=300, APY=0.0631, name='DP17'),
            Loan(20888.36, monthly=300, APY=0.0700, name='DP18'),

            # HAPO Accounts
            Asset(20000,    monthly=500,    APY=0.0011, name='HAPO S0'),
            Asset(2000,     monthly=0,      APY=0.0005, name='HAPO C0'),
            ])

    print(portfolio)

    for month in range(months):
        portfolio.step()
        print(f'Month number {1+month}:\t{portfolio}')

if __name__ == '__main__':
    main()

