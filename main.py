import click
import re
import sys
import os
import math
import functools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
ax = plt.axes()

from accounts import Debt, Asset, Portfolio, Loan, PNNL401K

@click.command()
@click.option('-m', '--months', type=int, default=12,
        help='Number of months to simulate')
@click.option('-i', '--interval', type=int, default=0,
        help='Number of iterations to skip between printing')
@click.option('-p', '--plot', is_flag=True, default=False,
        help='Flag to plot pf over time period')
def main(months, interval, plot):

    pf = Portfolio([
            Loan(2243, monthly=20,  APY=0.0367, name='DU16'),
            Asset(15000,    monthly=500,    APY=0.0011, name='S0'),
            Asset(2000,     monthly=0,      APY=0.0005, name='C0'),
            ])

    i = 0
    print(pf)

    for month in range(months):

        if month == 2:
            pf.extend([
                # Personal federal loans
                Loan(2750, monthly=10, APY=0.0505, name='DS18'),
                # Loan(1073, monthly=0, APY=0.0505, name='DU18'), # paid off 2/6
                Loan(4500, monthly=10, APY=0.0445, name='DS17'),
                # Loan(2200, monthly=0, APY=0.0445, name='DU17'), # paid off 2/6
                Loan(3500, monthly=10, APY=0.0376, name='DS16'),

                # Private parent plus loans
                # Loan(21801.79, monthly=500, APY=0.0631, name='DP17'),
                Loan(0, monthly=500, APY=0.0631, name='DP17'),
                Loan(20888.36, monthly=500, APY=0.0700, name='DP18'),
                
                PNNL401K(0, monthly=200, APY=0.065, name='PNNL401k'),
                ])
            pf.assets['S0'].monthly = 300

        if month == 24:
            pf.assets['S0'].monthly += 100
            pf.debts['DP17'].monthly += 100
            pf.debts['DP18'].monthly += 100
            pf.assets['PNNL401k'].monthly += 100
            pf.append(Loan(15000, monthly=500, APY=0.053, name='CarLoan'))

        if month == 36:
            pf.assets['S0'].monthly += 100
            pf.debts['DP17'].monthly += 100
            pf.debts['DP18'].monthly += 100
            pf.assets['PNNL401k'].monthly += 100

        pf.step()
        i += 1
        if i > interval:
            print(f'Month number {1+month}:\t{pf}')
            i = 0

        if plot:
            pf.plt()
            # pf.plt_finegrain()

    print('Done!')

    # Keep plot open at the end
    plt.show(block=True)

if __name__ == '__main__':
    main()
