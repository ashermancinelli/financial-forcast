from accounts import Debt, Asset, Portfolio, Loan, PNNL401K, Callback

def create_portfolio():
    pf = Portfolio([
            Loan(2243,	    monthly=20,     APY=0.0367, name='DU16'),
            Asset(15000,    monthly=500,    APY=0.0011, name='S0'),
            Asset(2000,     monthly=0,      APY=0.0005, name='C0'),
            ])

    pf.append_at(2,     Loan(2750,	monthly=10,     APY=0.0505, name='DS18'))
    # pf.append_at(2, Loan(1073,	monthly=0, APY=0.0505, name='DU18')) # paid off 2/6
    pf.append_at(2,     Loan(4500,	monthly=10,     APY=0.0445, name='DS17'))
    # pf.append_at(2, Loan(2200,	monthly=0, APY=0.0445, name='DU17')) # paid off 2/6
    pf.append_at(2,     Loan(3500,	monthly=10,     APY=0.0376, name='DS16'))
    pf.append_at(2,     Loan(21801.79,  monthly=500,    APY=0.0631, name='DP17'))
    pf.append_at(2,     Loan(20888.36,  monthly=500,    APY=0.0700, name='DP18'))
    pf.append_at(2,     PNNL401K(0,	monthly=200,    APY=0.0650, name='PNNL401k'))
    pf.append_at(24,    Loan(15000,     monthly=500,    APY=0.0530, name='CarLoan'))

    pf.add_callback(2,  lambda s: s.set('S0',       'monthly', 300))

    pf.add_callback(8,  lambda s: s.call('DP17',    'one_time_payment', 25000))
    pf.add_callback(8,  lambda s: s.set('DS17',     'monthly', 250))
    pf.add_callback(8,  lambda s: s.set('DS16',     'monthly', 250))

    pf.add_callback(24, lambda s: s.set('S0',       'monthly', 400))
    pf.add_callback(24, lambda s: s.set('DP17',     'monthly', 110))
    pf.add_callback(24, lambda s: s.set('DP18',     'monthly', 110))
    pf.add_callback(24, lambda s: s.set('PNNL401k', 'monthly', 100))

    pf.add_callback(36, lambda s: s.set('S0',       'monthly', 500))
    pf.add_callback(36, lambda s: s.set('DP17',     'monthly', 210))
    pf.add_callback(36, lambda s: s.set('DP18',     'monthly', 210))
    pf.add_callback(36, lambda s: s.set('PNNL401k', 'monthly', 200))
    
    return pf
