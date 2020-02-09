
class Account:

    def __init__(self, principle, monthly, APY, name):
        self.balance = principle
        self.principle = principle
        self.monthly = monthly
        self.APY = APY
        self.rate = APY/12
        self.name = name

    def interest(self):
        return self.balance - self.principle

    def __str__(self):
        return f'{self.name} ({type(self).__name__}): {self.balance}'

    def __repr__(self):
        return str(self)

    def __float__(self):
        return float(self.balance)
