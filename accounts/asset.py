
from collections import namedtuple

from .account import Account

class Asset(Account):

    def __init__(self, principle, monthly, APY, name):
        super().__init__(principle, monthly, APY, name)

    def step_month(self):
        self.balance += self.monthly
        self.balance *= 1 + self.rate

    def one_time_payment(self, amount):
        self.balance += amount
    
class PNNL401K(Asset):

    '''
    TODO:
        implement traditional/roth plans with current/projected
        taxout rates.
    '''
    def __init__(self, principle, monthly, APY, name, traditional=False):
        self.traditional = traditional
        super().__init__(principle, monthly, APY=APY, name=name)

class MoneyMarket(Asset):
    Rate = namedtuple('Range', ['range', 'APY'])
    APYs = [
            Rate((0,        2499.99),   0.0000),
            Rate((2500,     4999.99),   0.0020),
            Rate((5000,     14999.99),  0.0025),
            Rate((15000,    24999.99),  0.0030),
            Rate((25000,    49999.99),  0.0040),
            Rate((50000,    99999.99),  0.0050),
            Rate((100000,   999999),    0.0055),
            ]

    def __init__(self, principle, monthly, name):
        for i in APYs:
            if i.range[0] <= principle <= i.range[1]:
                APY = i.APY
        super().__init__(principle, monthly, APY, name)

class CertificateAsset(Asset):
    APYs = {
            6: .0075,
            12: .0149,
            18: .0164,
            24: .0174,
            30: .0184,
            36: .0189,
            48: .0194,
            60: .0199,
            }

    def __init__(self, principle, months, name):
        assert months in APYs.keys(), 'Number of months must be valid.'
        self.isAccessable = False
        APY = APYs[months]
        super().__init__(principle, monthly=0, APY=APY, name=name)
