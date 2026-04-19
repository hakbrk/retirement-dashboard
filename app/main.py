import streamlit as st
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Retirement Dashboard", page_icon="📊", layout="wide")

ACCOUNT_TYPES = ["Brokerage", "Traditional IRA", "Roth IRA", "401k", "401k Roth", "Savings", "Pension", "Social Security"]
OWNERS = ["Self", "Spouse"]

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

def calculate_tax(income, filing_status="Married Filing Jointly"):
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

def main():
    st.title("📊 Retirement Cashflow Dashboard")
    st.markdown("---")

    if "user_data" not in st.session_state:
        st.session_state.user_data = {
            "self_dob": None,
            "spouse_dob": None,
            "target_age": 100,
            "reserve_years": 2,
            "accounts": [],
            "expenses": [],
            "inflation_rate": 0.03,
            "state_tax_rate": 0.0,
        }

    col1, col2 = st.columns([2, 1])

    with col1:
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Personal", "💰 Accounts", "📋 Expenses", "📈 Projection"])

        with tab1:
            st.subheader("Personal Information")
            c1, c2 = st.columns(2)
            with c1:
                self_dob = st.date_input("Your Date of Birth", value=None, key="self_dob")
            with c2:
                spouse_dob = st.date_input("Spouse Date of Birth", value=None, key="spouse_dob")

            c3, c4, c5 = st.columns(3)
            with c3:
                target_age = st.number_input("Plan to Age", value=100, min_value=60, max_value=120)
            with c4:
                reserve_years = st.number_input("Reserve Years at End", value=2, min_value=0, max_value=10)
            with c5:
                inflation_rate = st.number_input("Inflation Rate", value=0.03, min_value=0.0, max_value=0.2, step=0.005, format="%.3f")

            c6, c7 = st.columns(2)
            with c6:
                filing_status = st.selectbox("Filing Status", ["Married Filing Jointly", "Single"])
            with c7:
                state_tax_rate = st.number_input("State Tax Rate", value=0.0, min_value=0.0, max_value=0.15, step=0.005, format="%.3f")

            if self_dob:
                self_age = calculate_age(self_dob)
                st.success(f"You are {self_age} years old")
            if spouse_dob:
                spouse_age = calculate_age(spouse_dob)
                st.success(f"Spouse is {spouse_age} years old")

            st.session_state.user_data.update({
                "self_dob": self_dob,
                "spouse_dob": spouse_dob,
                "target_age": target_age,
                "reserve_years": reserve_years,
                "inflation_rate": inflation_rate,
                "filing_status": filing_status,
                "state_tax_rate": state_tax_rate,
            })

        with tab2:
            st.subheader("Add Account")
            with st.form("add_account"):
                c1, c2 = st.columns(2)
                with c1:
                    acct_name = st.text_input("Account Name")
                with c2:
                    acct_type = st.selectbox("Account Type", ACCOUNT_TYPES)

                c3, c4 = st.columns(2)
                with c3:
                    owner = st.selectbox("Owner", OWNERS)
                with c4:
                    balance = st.number_input("Balance ($)", min_value=0.0, step=1000.0)

                c5, c6 = st.columns(2)
                with c5:
                    return_rate = st.number_input("Expected Return (%)", value=0.06, min_value=0.0, max_value=0.2, step=0.005, format="%.3f")
                with c6:
                    cola = st.checkbox("COLA Adjusted?", value=False)

                submit = st.form_submit_button("Add Account")

            st.subheader("Your Accounts")
            if "accounts" not in st.session_state:
                st.session_state.accounts = []

            accounts = st.session_state.accounts

            if accounts:
                df = pd.DataFrame(accounts)
                st.dataframe(df, use_container_width=True, hide_index=True)

                st.subheader("Edit Account")
                edit_idx = st.selectbox("Select account to edit", range(len(accounts)), format_func=lambda i: accounts[i]["name"] if i < len(accounts) else "")
                if edit_idx is not None:
                    acc = accounts[edit_idx]
                    c1, c2 = st.columns(2)
                    with c1:
                        new_balance = st.number_input("New Balance", value=acc["balance"], min_value=0.0)
                    with c2:
                        new_return = st.number_input("New Return Rate", value=acc["return_rate"], min_value=0.0, max_value=0.2, step=0.005, format="%.3f")
                    if st.button("Update"):
                        accounts[edit_idx]["balance"] = new_balance
                        accounts[edit_idx]["return_rate"] = new_return
                        st.rerun()
            else:
                st.info("No accounts added yet")

        with tab3:
            st.subheader("Add Expense")
            with st.form("add_expense"):
                c1, c2 = st.columns(2)
                with c1:
                    expense_name = st.text_input("Expense Name")
                with c2:
                    expense_amount = st.number_input("Amount ($)", min_value=0.0, step=100.0)

                c3, c4 = st.columns(2)
                with c3:
                    start_age = st.number_input("Start Age", min_value=0, max_value=120, value=51)
                with c4:
                    end_age = st.number_input("End Age", min_value=0, max_value=120, value=100)

                c5, c6 = st.columns(2)
                with c5:
                    freq = st.selectbox("Frequency", ["One-time", "Annual", "Every 5 Years", "Monthly"])
                with c6:
                    inflation_adj = st.checkbox("Inflation Adjusted?", value=True)

                submit2 = st.form_submit_button("Add Expense")

            st.subheader("Your Expenses")
            if "expenses" not in st.session_state:
                st.session_state.expenses = []

            expenses = st.session_state.expenses

            if expenses:
                df = pd.DataFrame(expenses)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No expenses added yet")

        with tab4:
            st.subheader("Projection Results")

            if not self_dob or not accounts:
                st.warning("Please enter your birth date and add at least one account")
            else:
                results = run_projection(
                    self_dob, spouse_dob, target_age, reserve_years,
                    accounts, expenses, inflation_rate, filing_status, state_tax_rate
                )
                display_results(results)

    with col2:
        st.subheader("Summary")
        total_assets = sum(a["balance"] for a in accounts)
        st.metric("Total Assets", f"${total_assets:,.0f}")

        taxable = sum(a["balance"] for a in accounts if a["type"] in ["Brokerage", "Savings"])
        tax_deferred = sum(a["balance"] for a in accounts if a["type"] in ["Traditional IRA", "401k"])
        roth = sum(a["balance"] for a in accounts if a["type"] in ["Roth IRA", "401k Roth"])
        pension = sum(a["balance"] for a in accounts if a["type"] == "Pension")
        ss = sum(a["balance"] for a in accounts if a["type"] == "Social Security")

        st.write("**By Account Type:**")
        st.write(f"- Taxable: ${taxable:,.0f}")
        st.write(f"- Tax-Deferred: ${tax_deferred:,.0f}")
        st.write(f"- Roth: ${roth:,.0f}")
        st.write(f"- Pension: ${pension:,.0f}")
        st.write(f"- Social Security: ${ss:,.0f}")

def run_projection(self_dob, spouse_dob, target_age, reserve_years, accounts, expenses, inflation_rate, filing_status, state_tax_rate):
    from datetime import date

    results = []
    base_year = date.today().year

    self_age = calculate_age(self_dob)
    spouse_age = calculate_age(spouse_dob) if spouse_dob else None

    younger_age = min(self_age, spouse_age) if spouse_age else self_age
    older_age = max(self_age, spouse_age) if spouse_age else self_age

    account_balances = {i: a["balance"] for i, a in enumerate(accounts)}

    for year_offset in range(target_age - younger_age + 1):
        current_self_age = self_age + year_offset
        current_spouse_age = (spouse_age + year_offset) if spouse_age else None

        current_younger_age = younger_age + year_offset

        if current_younger_age > 100:
            break

        income_from_accounts = 0
        withdrawals = {}
        rmd_amount = 0

        for i, acc in enumerate(accounts):
            balance = account_balances.get(i, acc["balance"])
            return_rate = acc["return_rate"]

            if acc["type"] == "Pension":
                income = balance
                if not acc.get("cola"):
                    income *= (1 + inflation_rate) ** year_offset
                income_from_accounts += income
            elif acc["type"] == "Social Security":
                income = balance
                if not acc.get("cola"):
                    income *= (1 + inflation_rate) ** year_offset
                income_from_accounts += income
            else:
                growth = balance * return_rate
                account_balances[i] = balance + growth

                access_age = 59.5
                if acc["owner"] == "Spouse" and current_spouse_age:
                    access_age = min(access_age, 59.5)

                if current_self_age >= access_age or (current_spouse_age and current_spouse_age >= access_age):
                    if acc["type"] in ["Traditional IRA", "401k"] and current_self_age >= 73:
                        rmd = calculate_rmd(current_self_age, account_balances[i])
                        rmd_amount += rmd
                        account_balances[i] -= rmd
                        income_from_accounts += rmd

        total_expenses = 0
        for exp in expenses:
            if exp["start_age"] <= current_younger_age <= exp["end_age"]:
                amount = exp["amount"]
                if exp.get("inflation_adj", True):
                    amount *= (1 + inflation_rate) ** year_offset
                total_expenses += amount

        gross_income = income_from_accounts + total_expenses
        federal_tax = calculate_tax(gross_income, filing_status)
        state_tax = gross_income * state_tax_rate

        after_tax = gross_income - federal_tax - state_tax

        results.append({
            "year": base_year + year_offset,
            "age": current_younger_age,
            "income": income_from_accounts,
            "rmd": rmd_amount,
            "expenses": total_expenses,
            "gross": gross_income,
            "federal_tax": federal_tax,
            "state_tax": state_tax,
            "after_tax": after_tax,
            "total_assets": sum(account_balances.values()),
        })

    return results

def display_results(results):
    if not results:
        return

    df = pd.DataFrame(results)
    df["year"] = df["year"].astype(int)
    df["age"] = df["age"].astype(int)

    st.subheader("Yearly After-Tax Spendable")

    cols = st.columns(2)
    with cols[0]:
        st.metric("Average Annual Spend", f"${df['after_tax'].mean():,.0f}")
    with cols[1]:
        st.metric("First Year Spend", f"${df.iloc[0]['after_tax']:,.0f}")

    st.subheader("Projected Spend Over Time")
    chart_data = df[["year", "after_tax", "age"]].copy()
    st.line_chart(chart_data.set_index("year")["after_tax"])

    st.subheader("Detailed Projection")
    display_df = df.copy()
    for col in ["income", "rmd", "expenses", "gross", "federal_tax", "state_tax", "after_tax", "total_assets"]:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    years_negative = len(df[df["after_tax"] < 0])
    if years_negative > 0:
        st.error(f"⚠️ Projection goes negative in {years_negative} years!")
    else:
        st.success("✓ Money lasts through target age!")

if __name__ == "__main__":
    main()