
from .account import Account

class Debt(Account):

    def step_month(self, additional_payment=0):
        self.balance -= self.monthly
        self.balance -= additional_payment
        if self.balance <= 0:
            # Account no longer accrues interest
            self.rate = -1
        self.balance *= 1 + self.rate

    def one_time_payment(self, amount):
        self.balance -= amount
    
class Loan(Debt):

    def __init__(self, principle, monthly, APY, name):
        super().__init__(principle, monthly, APY, name)
