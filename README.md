# finance-mauritius

Useful functions for Mauritius banks and financials institutions like MRA (Mauritius Revenue Authority)

```
pip install finance-mauritius
```

Export your data in Excel format

```python
>>> from finance_mauritius.mcb import MCB
>>> MCB.process_csv('mcb.CSV')
{
    'df': <polars df>, 
    'info': {
        'account_number': '00000000001', 
        'account_currency': 'MUR', 
        'opening_balance': '0.00', 
        'closing_balance': '15000.00', 
        'specified_period': '31-01-2024 - 31-03-2024', 
        'money_in': Decimal('48000.00'), 
        'money_out': Decimal('25915.00')
}

>>> MCB.csv_money_in()
{
    'Interbank Transfer <redacted> fare INTERNET BANKING TRANSFER': Decimal(10000.00), 
    'Instant Payment MCBL40329424554O': Decimal(10000.00)
}
>>> MCB.csv_money_out()
{
    'JUICE Transfer <redacted>': Decimal(1000.00), 
    'JUICE Transfer <redacted>': Decimal(2000.00), 
    'JUICE Transfer <redacted>': Decimal(2000.00)
}
>>> from finance_mauritius.mcb import SBM
>>> SBM.process_csv('SBM.csv')
{
    'info': {
        'account_number': '00000000000001', 
        'date_from': '03032024', 
        'date_to': '04012024', 
        'transactions_for': '-', 
        'last_n_transactions': '-', 
        'money_in': Decimal(20000.00),
        'money_out': Decimal(10000.00),
        }, 
    'df': <polars df>
}
>>> SBM.csv_money_in()
{   
    'SOM3R3F:<redacted>': Decimal('10000.00'), 
    'MCBLMUMU/<redacted>': Decimal('10000.00')
}
>>> SBM.csv_money_out()
{
    '<redacted> NON SBM POS': Decimal('1000.00'), 
    'ATM Withdrawal - <redacted>': Decimal('9000.00')
}
```

## Options

```

```