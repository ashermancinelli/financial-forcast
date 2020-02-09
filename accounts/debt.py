
from .account import Account

class Debt(Account):
    pass

class Loan(Debt):

    def __init__(self, principle, monthly, APY, name):
        super().__init__(principle, monthly, APY, name)

    def step_month(self, additional_payment=0):
        self.balance -= ( self.monthly + additional_payment )
        self.balance += ( self.principle * self.APY )

