from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_age(birth_date):
    today = date.today()
    return relativedelta(today, birth_date).years

def calculate_rmd(age, balance):
    rmd_table = {
        72: 27, 73: 26, 74: 25, 75: 24, 76: 23, 77: 22, 78: 21, 79: 20, 80: 19,
        81: 18, 82: 17, 83: 16, 84: 15, 85: 14, 86: 13, 87: 12, 88: 11, 89: 10,
        90: 9, 91: 8, 92: 7, 93: 6, 94: 5, 95: 4, 96: 3, 97: 2, 98: 1, 99: 1, 100: 1
    }
    divisor = rmd_table.get(age, 1)
    return balance / divisor if divisor > 0 else balance

def calculate_federal_tax(income, filing_status="Married Filing Jointly"):
    brackets = [
        (23850, 0.10),
        (96950, 0.12),
        (206700, 0.22),
        (394400, 0.24),
        (501950, 0.32),
        (751600, 0.35),
        (float('inf'), 0.37)
    ] if filing_status == "Married Filing Jointly" else [
        (11950, 0.10),
        (48450, 0.12),
        (103350, 0.22),
        (197300, 0.24),
        (250950, 0.35),
        (677050, 0.37),
        (float('inf'), 0.37)
    ]
    tax = 0
    remaining = income
    prev_limit = 0
    for limit, rate in brackets:
        if remaining <= 0:
            break
        taxable = min(remaining, limit - prev_limit)
        if taxable > 0:
            tax += taxable * rate
            remaining -= taxable
        prev_limit = limit
    return tax

def can_withdraw(account_type, age, owner="Self"):
    access_rules = {
        "Brokerage": 0,
        "Savings": 0,
        "Traditional IRA": 59.5,
        "Roth IRA": 59.5,
        "401k": 59.5,
        "401k Roth": 59.5,
    }
    min_age = access_rules.get(account_type, 0)
    return age >= min_age

def is_tax_deferred(account_type):
    return account_type in ["Traditional IRA", "401k"]

def is_roth(account_type):
    return account_type in ["Roth IRA", "401k Roth"]

def is_taxable(account_type):
    return account_type in ["Brokerage", "Savings"]

def calculate_withdrawal_order(ages):
    return ["Social Security", "Pension", "Tax-Deferred", "Roth", "Taxable"]