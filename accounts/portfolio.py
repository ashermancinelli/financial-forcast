
from functools import reduce
from collections import namedtuple
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time

from .asset import Asset
from .debt import Debt

Callback = namedtuple('Callback', ['month', 'callback'])

class Portfolio:

    def __init__(self, accounts=list(), plot=False):
        _assets = list(filter(lambda x: isinstance(x, Asset), accounts))
        _debts = list(filter(lambda x: isinstance(x, Debt), accounts))
        self.assets = { a.name: a for a in _assets }
        self.debts = { a.name: a for a in _debts }

        # For plotting accounts grouped by type
        self.asset_history = list()
        self.debt_history = list()

        # For plotting all accounts individually
        self.asset_history_finegrain = list()
        self.debt_history_finegrain = list()

        self.plot = plot
        self.callbacks = list()
        self.month = 0
        self._step_history()
        self.first_draw = True

    def __enter__(self):
        return self

    def add_callback(self, month, f):
        self.callbacks.append(Callback(month, f))

    def apply_callbacks(self):
        del_idxs = list()
        for index, (month, f) in enumerate(self.callbacks):
            if month == self.month:
                f(self)
                del_idxs.append(index)

        for i in reversed(del_idxs):
            self.callbacks.pop(i)

    def append(self, acc):
        if isinstance(acc, Asset):
            self.assets[acc.name] = acc
        elif isinstance(acc, Debt):
            self.debts[acc.name] = acc

    def append_at(self, month, acc):
        self.add_callback(month, lambda s: s.append(acc))

    def extend(self, accs):
        for acc in accs:
            if isinstance(acc, Asset):
                self.assets[acc.name] = acc
            elif isinstance(acc, Debt):
                self.debts[acc.name] = acc

    def balance(self, key=None):
        if key is None:
            return self.networth
        else:
            if key in self.assets.keys():
                return self.assets[key].balance
            elif key in self.debts.keys():
                return self.debts[key].balance
            else:
                False

    def set(self, name, key, value):
        if name in self.assets.keys():
            self.assets[name].__setattr__(key, value)
        elif name in self.debts.keys():
            self.debts[name].__setattr__(key, value)

    def call(self, name, method, *args):
        try:
            if name in self.assets.keys():
                m = getattr(self.assets[name], method)
            elif name in self.debts.keys():
                m = getattr(self.debts[name], method)

            m(*args)
        except AttributeError:
            print('Attempted call on method that does not exist.')
            exit(1)

    @property
    def asset_total(self):
        return reduce(lambda a, b: float(a) + float(b), self.assets.values(), 0)

    @property
    def debt_total(self):
        return reduce(lambda a, b: float(a) + float(b), self.debts.values(), 0)

    @property
    def networth(self):
        return self.asset_total - self.debt_total

    def __str__(self):
        return f'Assets: {self.asset_total:.2f}\t' \
            f'Debts: {self.debt_total:.2f}\t' \
            f'Net Worth: {self.networth:.2f}'

    def _step_history(self):
        self.month += 1
        self.asset_history_finegrain.append(
                { k: v.balance for k, v in self.assets.items() })
        self.debt_history_finegrain.append(
                { k: v.balance for k, v in self.debts.items() })

        self.asset_history.append(self.asset_total)
        self.debt_history.append(self.debt_total)

    def step(self):
        self.apply_callbacks()
        for k in self.assets.keys():
            self.assets[k].step_month()

        for k in self.debts.keys():
            self.debts[k].step_month()

        self._step_history()
        if self.plot:
            self.plt()

    def plt_finegrain(self):
        xs = list(range(self.month))

        for name in self.assets.keys():
            history = list()
            for i in self.asset_history_finegrain:
                if name in i.keys():
                    history.append(i[name])
                else:
                    history.append(0)
            plt.plot(xs, history, label=name)
            plt.pause(0.0001)

        for name in self.debts.keys():
            history = list()
            for i in self.debt_history_finegrain:
                if name in i.keys():
                    history.append(i[name])
                else:
                    history.append(0)

            plt.plot(xs, history, label=name)
            plt.pause(0.0001)

        ax = plt.gca()
        leg = ax.get_legend()
        if leg:
            leg.remove()
        plt.legend([*self.assets.keys(), *self.debts.keys()])
        if self.first_draw:
            plt.ylabel('$ Value')
            plt.xlabel('Months')
            plt.title('Debts Finegrain')
            self.first_draw = False

    def plt(self):
        xs = list(range(self.month))
        plt.plot(xs, self.asset_history, 'g-', label='Assets')
        plt.pause(0.0001)
        plt.plot(xs, self.debt_history, 'b-', label='Debts')
        plt.pause(0.0001)
        nw_history = list(map(
                lambda a: a[0] - a[1],
                zip(self.asset_history, self.debt_history)
                ))

        plt.plot(xs, nw_history, 'r-', label='Net Worth')
        plt.pause(0.0001)

        if self.first_draw:
            plt.ylabel('$ Value')
            plt.xlabel('Months')
            plt.title('Overview plot')
            plt.legend()
            self.first_draw = False

    def __exit__(self, type, value, traceback):
        if self.plot:
            plt.show(block=True)
