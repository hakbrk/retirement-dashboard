# Retirement Cashflow Dashboard - Project Plan

## Goal
Replace Hawkins_Cashflow_Tool_Full_Rev26.xlsm with a sophisticated, trustworthy web-based dashboard that works on desktop and mobile.

## Users
- Primary: You
- Secondary: Spouse (view on mobile)

## Repo
https://github.com/hakbrk/retirement-dashboard

---

## Task List

### Phase 1 - MVP (Complete)
- [x] Personal data input (DOB, target age, reserve years)
- [x] Account input form (Brokerage, IRA, 401k, Roth, Savings, Pension, SS)
- [x] Expense tracking (one-time, recurring, inflation-adjusted)
- [x] Basic projection to target age
- [x] Account access + RMD rules
- [x] After-tax spend output (federal tax)
- [x] Responsive dashboard view

### Phase 2 - Current
- [ ] Social Security input (monthly benefit, claiming age)
- [ ] Pension input (monthly amount, COLA flag)
- [ ] State tax input (per-account or flat rate)
- [ ] Add scenario comparison (retire now vs later)
- [ ] Save/load user data (localStorage or JSON file)

### Phase 3 - Risk & Stress Testing
- [ ] Risk tolerance selector (Aggressive/Moderate/Conservative return rates)
- [ ] Monte Carlo simulation
- [ ] Stress test results (best/expected/worst case)
- [ ] Band visualization

### Phase 4 - Advanced
- [ ] Roth conversion scenario
- [ ] Tax optimization suggestions
- [ ] Rebalancing automation rules
- [ ] Investment-level modeling
- [ ] Rebalancing events (home sale, etc.)

---

## Core Features

### 1. Account Aggregation
- Input: Brokerage, Savings, IRA, 401k, Roth, Pension, Social Security
- Fields: Account name, type, balance, owner, expected return rate

### 2. Personal Data
- Date of birth (self + spouse)
- Target end age (configurable, e.g., 100)
- Reserve requirement (e.g., 2 years expenses at end)
- Claiming ages for Social Security

### 3. Cashflow Projection Engine
- Age-based spending limits per person
- Account access rules (59.5 for retirement accounts, pension rules)
- RMD calculations (Required Minimum Distributions)
- One-time events (one-off expenses)
- Recurring events (car every 5 years, etc.)

### 4. Inflation & Income Types
- Inflation-adjusted income (COLA)
- Fixed income (non-COLA pension)
- Per-account return rate assumptions

### 5. Risk Tolerance Modeling
- Return bands: Aggressive / Moderate / Conservative
- Stress testing across scenarios
- Monte Carlo or sensitivity analysis

### 6. Scenario Comparison
- Compare: retire now vs later, spend levels, Roth conversion strategies
- Side-by-side results

### 7. Rebalancing Rules
- Annual review: excess savings → investments
- Event-based: one-time inflows (home sale) → allocation

### 8. Tax-Aware Output
- **After-tax spendable amounts** (critical)
- Federal tax brackets
- State tax (flat rate or input)
- Tax-deferred vs Roth vs taxable order optimization

### 9. Mobile-Friendly Dashboard
- Responsive design
- Primary: view on mobile
- Full interaction on desktop

---

## Tech Stack
- Open source only
- Web app (Streamlit, browser-based)
- Python 3.12
- Quick prototype first (MVP), then iterate