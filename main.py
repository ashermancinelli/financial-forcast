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

from accounts import Debt, Asset, Portfolio, Loan, PNNL401K, Callback

import asher

@click.command()
@click.option('-m', '--months', type=int, default=-1,
        help='Number of months to simulate')
@click.option('-y', '--years', type=int, default=-1,
        help='Number of months to simulate')
@click.option('-i', '--interval', type=int, default=0,
        help='Number of iterations to skip between printing')
@click.option('-p', '--plot', is_flag=True, default=False,
        help='Flag to plot pf over time period')
def main(months, years, interval, plot):

    if years == -1 and months == -1:
        assert False, 'Must set either months or years.'
        exit(1)

    if years != -1:
        months = years * 12

    with asher.create_portfolio() as pf:
        pf.plot = True
        print(pf)
        i = 0
        for month in range(months):
            pf.step()
            i += 1
            if i > interval:
                print(f'Month number {1+month}:\t{pf}')
                i = 0

    print('Done!')

if __name__ == '__main__':
    main()
