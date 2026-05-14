import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Corporate Finance Learning Lab",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "round": 1,
    "cash": 200.0,
    "debt": 150.0,
    "equity": 350.0,
    "revenue": 500.0,
    "profit": 60.0,
    "stock_price": 100.0,
    "wacc": 0.10,
    "history": []
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# HELPER FUNCTIONS
# =========================================================

def generate_macro_conditions():

    return {
        "GDP Growth": random.choice([3, 4, 5, 6, 7]),
        "Inflation": random.choice([3, 4, 5, 6, 7, 8]),
        "Interest Rate": random.choice([5, 6, 7, 8, 9]),
        "Market Sentiment": random.choice(
            ["Bullish", "Neutral", "Bearish"]
        )
    }


def calculate_wacc(debt, equity, interest_rate):

    total = debt + equity

    if total == 0:
        return 0.10

    rd = interest_rate / 100
    re = 0.14
    tax = 0.30

    wacc = (
        (equity / total) * re +
        (debt / total) * rd * (1 - tax)
    )

    return round(wacc, 4)


def calculate_npv(
    initial_investment,
    annual_cashflow,
    discount_rate,
    years=5
):

    npv = -initial_investment

    for t in range(1, years + 1):

        npv += (
            annual_cashflow /
            ((1 + discount_rate) ** t)
        )

    return round(npv, 2)


def approximate_irr(
    investment,
    annual_cashflow
):

    irr = (
        (
            (annual_cashflow * 5) -
            investment
        ) / investment
    ) * 20

    return round(irr, 2)


def random_market_shock():

    shocks = [
        ("Economic Boom", 12),
        ("Interest Rate Hike", -6),
        ("Supply Chain Disruption", -8),
        ("Technology Breakthrough", 15),
        ("Recession", -12),
        ("Stable Economy", 3)
    ]

    return random.choice(shocks)


macro = generate_macro_conditions()

# =========================================================
# TITLE
# =========================================================

st.title("Corporate Finance Learning Lab")

st.markdown("""
An interactive corporate finance learning environment combining:

- Interactive textbook
- Experiential learning platform
- Financial simulation engine
- Strategic decision laboratory
- Pedagogical research tool

Students learn corporate finance concepts by experimenting with
realistic financial decisions and observing their implications
for shareholder wealth, risk, liquidity, and firm value.
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Simulation Status")

st.sidebar.metric(
    "Round",
    st.session_state.round
)

st.sidebar.header("Macroeconomic Conditions")

for key, value in macro.items():

    st.sidebar.write(
        f"**{key}:** {value}"
    )

# =========================================================
# COMPANY DASHBOARD
# =========================================================

st.header("Company Dashboard")

d1, d2, d3, d4 = st.columns(4)

d1.metric(
    "Cash",
    f"₹ {round(st.session_state.cash,2)} Cr"
)

d2.metric(
    "Debt",
    f"₹ {round(st.session_state.debt,2)} Cr"
)

d3.metric(
    "Profit",
    f"₹ {round(st.session_state.profit,2)} Cr"
)

d4.metric(
    "Stock Price",
    f"₹ {round(st.session_state.stock_price,2)}"
)

# =========================================================
# TABS
# =========================================================

(
    overview_tab,
    budgeting_tab,
    capital_structure_tab,
    dividend_tab,
    working_capital_tab,
    risk_tab,
    valuation_tab,
    financial_statement_tab,
    reflection_tab
) = st.tabs([

    "Financial Health Overview",
    "Capital Budgeting",
    "Capital Structure",
    "Dividend Policy",
    "Working Capital",
    "Risk Management",
    "Firm Valuation",
    "Financial Statements",
    "Strategic Reflection"
])

# =========================================================
# OVERVIEW TAB
# =========================================================

with overview_tab:

    st.header("Financial Health Overview")

    debt_equity_ratio = (
        st.session_state.debt /
        st.session_state.equity
    )

    current_ratio = (
        (st.session_state.cash + 100) / 80
    )

    o1, o2, o3 = st.columns(3)

    o1.metric(
        "Debt-to-Equity Ratio",
        round(debt_equity_ratio, 2)
    )

    o2.metric(
        "Current Ratio",
        round(current_ratio, 2)
    )

    o3.metric(
        "WACC",
        f"{round(st.session_state.wacc*100,2)}%"
    )

    with st.expander(
        "Learn About Financial Health"
    ):

        st.write("""
        Financial health evaluates the firm's:
        - liquidity,
        - profitability,
        - solvency,
        - leverage,
        - and operational sustainability.
        """)

        st.write("""
        Strong firms balance:
        - profitability,
        - growth,
        - and risk management.
        """)

# =========================================================
# CAPITAL BUDGETING
# =========================================================

with budgeting_tab:

    st.header("Capital Budgeting")

    st.latex(
        r'''NPV = \sum_{t=1}^{n}\frac{CF_t}{(1+r)^t} - C_0'''
    )

    st.latex(
        r'''IRR : NPV = 0'''
    )

    st.latex(
        r'''PI = \frac{PV\ of\ Future\ Cash\ Flows}{Initial\ Investment}'''
    )

    st.latex(
        r'''Payback\ Period = \frac{Initial\ Investment}{Annual\ Cash\ Inflow}'''
    )

    with st.expander(
        "Learn About Capital Budgeting"
    ):

        st.write("""
        Capital budgeting evaluates long-term investment projects.
        """)

        st.write("""
        Firms should generally:
        - accept positive NPV projects,
        - reject negative NPV projects.
        """)

        st.write("""
        NPV directly measures shareholder value creation.
        """)

    project = st.selectbox(
        "Select Project",
        [
            "Automation",
            "AI Expansion",
            "ESG Upgrade",
            "International Expansion"
        ]
    )

    scenario = st.selectbox(
        "Scenario Analysis",
        [
            "Best Case",
            "Base Case",
            "Worst Case"
        ]
    )

    investment_amount = st.slider(
        "Investment Amount (₹ Cr)",
        10,
        200,
        50
    )

    expected_cashflow = st.slider(
        "Expected Annual Cash Flow (₹ Cr)",
        5,
        100,
        20
    )

    discount_rate = st.slider(
        "Discount Rate (%)",
        5,
        20,
        10
    )

    if scenario == "Best Case":
        multiplier = 1.3

    elif scenario == "Worst Case":
        multiplier = 0.7

    else:
        multiplier = 1.0

    adjusted_cashflow = (
        expected_cashflow * multiplier
    )

    npv = calculate_npv(
        investment_amount,
        adjusted_cashflow,
        discount_rate / 100
    )

    irr = approximate_irr(
        investment_amount,
        adjusted_cashflow
    )

    payback = round(
        investment_amount /
        adjusted_cashflow,
        2
    )

    profitability_index = round(
        (
            npv + investment_amount
        ) / investment_amount,
        2
    )

    b1, b2, b3, b4 = st.columns(4)

    b1.metric("NPV", f"₹ {npv} Cr")
    b2.metric("IRR (%)", irr)
    b3.metric("Payback", payback)
    b4.metric("PI", profitability_index)

    if npv > 0:

        st.success("""
        The project is expected to create shareholder value.
        """)

    else:

        st.error("""
        The project may destroy shareholder value.
        """)

# =========================================================
# CAPITAL STRUCTURE
# =========================================================

with capital_structure_tab:

    st.header("Capital Structure")

    st.latex(
        r'''WACC = \frac{E}{V}R_e + \frac{D}{V}R_d(1-T)'''
    )

    st.latex(
        r'''R_e = R_f + \beta(R_m - R_f)'''
    )

    st.latex(
        r'''V_L = V_U + Tax\ Shield'''
    )

    st.latex(
        r'''Tax\ Shield = T_c \times Debt'''
    )

    with st.expander(
        "Learn About Capital Structure"
    ):

        st.write("""
        Capital structure refers to the mix of:
        - debt financing,
        - and equity financing.
        """)

        st.write("""
        Moderate debt creates tax advantages,
        but excessive leverage increases
        bankruptcy risk.
        """)

        st.write("""
        Firms balance:
        - tax shield benefits,
        - against financial distress costs.
        """)

    risk_free_rate = st.slider(
        "Risk-Free Rate (%)",
        2,
        10,
        5
    )

    beta = st.slider(
        "Beta",
        0.5,
        2.0,
        1.0
    )

    market_return = st.slider(
        "Expected Market Return (%)",
        6,
        18,
        12
    )

    cost_of_equity = round(
        risk_free_rate +
        beta * (
            market_return -
            risk_free_rate
        ),
        2
    )

    st.metric(
        "Cost of Equity (CAPM)",
        f"{cost_of_equity}%"
    )

    debt_financing = st.slider(
        "New Debt Raised (₹ Cr)",
        0,
        200,
        20
    )

    equity_financing = st.slider(
        "New Equity Raised (₹ Cr)",
        0,
        200,
        10
    )

    projected_debt = (
        st.session_state.debt +
        debt_financing
    )

    projected_equity = (
        st.session_state.equity +
        equity_financing
    )

    projected_wacc = calculate_wacc(
        projected_debt,
        projected_equity,
        macro["Interest Rate"]
    )

    de_ratio = round(
        projected_debt /
        projected_equity,
        2
    )

    ebit = st.slider(
        "EBIT (₹ Cr)",
        50,
        500,
        150
    )

    tax_rate = st.slider(
        "Corporate Tax Rate (%)",
        10,
        40,
        30
    )

    unlevered_cost = st.slider(
        "Unlevered Cost of Capital (%)",
        5,
        20,
        10
    )

    vu = round(
        (
            ebit *
            (1 - tax_rate/100)
        ) /
        (unlevered_cost/100),
        2
    )

    tax_shield = round(
        (tax_rate/100) *
        projected_debt,
        2
    )

    vl = round(
        vu + tax_shield,
        2
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Unlevered Firm Value",
        f"₹ {vu} Cr"
    )

    c2.metric(
        "Tax Shield",
        f"₹ {tax_shield} Cr"
    )

    c3.metric(
        "Levered Firm Value",
        f"₹ {vl} Cr"
    )

    if de_ratio < 0.5:

        st.success("""
        Conservative leverage reduces financial distress risk.
        """)

    elif de_ratio < 1.5:

        st.warning("""
        Moderate leverage may improve value through tax shields.
        """)

    else:

        st.error("""
        Excessive leverage may increase bankruptcy risk.
        """)

# =========================================================
# DIVIDEND POLICY
# =========================================================

with dividend_tab:

    st.header("Dividend Policy")

    st.latex(
        r'''Dividend\ Payout\ Ratio = \frac{Dividends}{Net\ Income}'''
    )

    st.latex(
        r'''Dividend\ Yield = \frac{Dividend\ Per\ Share}{Stock\ Price}'''
    )

    with st.expander(
        "Learn About Dividend Policy"
    ):

        st.write("""
        Dividend policy determines how much profit is:
        - distributed to shareholders,
        - versus retained for future growth.
        """)

        st.write("""
        Dividends may signal management confidence
        regarding future profitability.
        """)

    dividend_policy = st.selectbox(
        "Dividend Strategy",
        [
            "Stable Dividend",
            "High Dividend",
            "Residual Dividend",
            "No Dividend",
            "Share Buyback"
        ]
    )

    dividend_payout = st.slider(
        "Dividend Payout Ratio (%)",
        0,
        100,
        30
    )

    if dividend_policy == "High Dividend":

        st.warning("""
        High dividends improve investor satisfaction
        but reduce internal financing flexibility.
        """)

    elif dividend_policy == "No Dividend":

        st.info("""
        Retained earnings may support future growth.
        """)

# =========================================================
# WORKING CAPITAL
# =========================================================

with working_capital_tab:

    st.header("Working Capital Management")

    st.latex(
        r'''CCC = DIO + DSO - DPO'''
    )

    st.latex(
        r'''Operating\ Cycle = DIO + DSO'''
    )

    with st.expander(
        "Learn About Working Capital"
    ):

        st.write("""
        Working capital management ensures
        operational liquidity and efficiency.
        """)

        st.write("""
        Aggressive working capital policies
        may improve profitability but increase liquidity risk.
        """)

    credit_policy = st.selectbox(
        "Credit Policy",
        [
            "Strict",
            "Moderate",
            "Liberal"
        ]
    )

    inventory_policy = st.selectbox(
        "Inventory Policy",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    supplier_payment = st.selectbox(
        "Supplier Payment Strategy",
        [
            "Early",
            "Standard",
            "Delayed"
        ]
    )

    receivable_days = {
        "Strict": 30,
        "Moderate": 60,
        "Liberal": 90
    }[credit_policy]

    inventory_days = {
        "Low": 30,
        "Medium": 60,
        "High": 90
    }[inventory_policy]

    payable_days = {
        "Early": 20,
        "Standard": 45,
        "Delayed": 75
    }[supplier_payment]

    ccc = (
        inventory_days +
        receivable_days -
        payable_days
    )

    st.metric(
        "Cash Conversion Cycle",
        f"{ccc} Days"
    )

    if ccc > 90:

        st.warning("""
        High CCC may create liquidity stress.
        """)

# =========================================================
# RISK MANAGEMENT
# =========================================================

with risk_tab:

    st.header("Risk Management")

    st.latex(
        r'''Expected\ Return = Risk\ Free\ Rate + Risk\ Premium'''
    )

    with st.expander(
        "Learn About Risk Management"
    ):

        st.write("""
        Firms face:
        - interest rate risk,
        - foreign exchange risk,
        - liquidity risk,
        - and commodity price risk.
        """)

        st.write("""
        Hedging reduces uncertainty but may involve costs.
        """)

    hedge_policy = st.selectbox(
        "Hedging Strategy",
        [
            "No Hedging",
            "Partial Hedging",
            "Full Hedging"
        ]
    )

    risk_type = random.choice([
        "Interest Rate Risk",
        "FX Risk",
        "Commodity Risk",
        "Liquidity Risk"
    ])

    st.metric(
        "Current Major Risk",
        risk_type
    )

# =========================================================
# FIRM VALUATION
# =========================================================

with valuation_tab:

    st.header("Firm Valuation")

    st.latex(
        r'''Firm\ Value = \sum_{t=1}^{n}\frac{FCFF_t}{(1+WACC)^t}'''
    )

    st.latex(
        r'''Terminal\ Value = \frac{FCFF_{n+1}}{WACC-g}'''
    )

    with st.expander(
        "Learn About Firm Valuation"
    ):

        st.write("""
        Firm valuation estimates the intrinsic value
        of the company using future cash flows.
        """)

        st.write("""
        Discounted cash flow models are widely used
        in investment banking and corporate finance.
        """)

    estimated_value = round(
        st.session_state.profit /
        st.session_state.wacc,
        2
    )

    st.metric(
        "Estimated Firm Value",
        f"₹ {estimated_value} Cr"
    )

# =========================================================
# RUN SIMULATION
# =========================================================

st.header("Run Simulation")

if st.button("Run Simulation Round"):

    shock_name, shock_effect = (
        random_market_shock()
    )

    revenue_growth = np.random.uniform(
        0.02,
        0.15
    )

    if credit_policy == "Liberal":
        revenue_growth += 0.03

    updated_revenue = (
        st.session_state.revenue *
        (1 + revenue_growth)
    )

    updated_profit = (
        updated_revenue * 0.12
    ) + shock_effect

    dividend_amount = (
        updated_profit *
        (dividend_payout / 100)
    )

    updated_cash = (
        st.session_state.cash
        + updated_profit
        - investment_amount
        + debt_financing
        + equity_financing
        - dividend_amount
    )

    updated_stock_price = max(
        10,
        st.session_state.stock_price +
        (updated_profit / 10)
    )

    st.session_state.revenue = updated_revenue
    st.session_state.profit = updated_profit
    st.session_state.cash = updated_cash
    st.session_state.stock_price = updated_stock_price
    st.session_state.debt = projected_debt
    st.session_state.equity = projected_equity
    st.session_state.wacc = projected_wacc

    st.session_state.history.append({

        "Round": st.session_state.round,
        "Revenue": updated_revenue,
        "Profit": updated_profit,
        "Cash": updated_cash,
        "Stock Price": updated_stock_price
    })

    st.session_state.round += 1

    st.success(
        f"Simulation Completed: {shock_name}"
    )

# =========================================================
# FINANCIAL STATEMENTS
# =========================================================

with financial_statement_tab:

    st.header("Financial Statements")

    with st.expander(
        "Learn About Financial Statements"
    ):

        st.write("""
        Corporate finance decisions ultimately affect:
        - profitability,
        - liquidity,
        - leverage,
        - and shareholder equity.
        """)

    income_statement = pd.DataFrame({

        "Item": [
            "Revenue",
            "Operating Profit",
            "Interest Expense",
            "Net Profit"
        ],

        "Amount": [

            round(st.session_state.revenue,2),
            round(st.session_state.profit,2),
            round(st.session_state.debt * 0.08,2),

            round(
                st.session_state.profit -
                (st.session_state.debt * 0.08),
                2
            )
        ]
    })

    balance_sheet = pd.DataFrame({

        "Item": [
            "Cash",
            "Debt",
            "Equity"
        ],

        "Amount": [

            round(st.session_state.cash,2),
            round(st.session_state.debt,2),
            round(st.session_state.equity,2)
        ]
    })

    fs1, fs2 = st.columns(2)

    with fs1:

        st.subheader("Income Statement")
        st.dataframe(income_statement)

    with fs2:

        st.subheader("Balance Sheet")
        st.dataframe(balance_sheet)

# =========================================================
# STRATEGIC REFLECTION
# =========================================================

with reflection_tab:

    st.header("Strategic Reflection")

    st.write("""
    Reflection helps students connect:
    - theory,
    - managerial judgment,
    - and financial outcomes.
    """)

    st.text_area(
        "How did your investment decision impact shareholder wealth?",
        height=150
    )

    st.text_area(
        "Did leverage improve firm value or increase financial risk excessively?",
        height=150
    )

    st.text_area(
        "How did working capital decisions affect liquidity and operational efficiency?",
        height=150
    )

    st.text_area(
        "Would you change your dividend policy under different macroeconomic conditions?",
        height=150
    )

# =========================================================
# RESULTS VISUALIZATION
# =========================================================

st.header("Simulation Performance")

if len(st.session_state.history) > 0:

    df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(df)

    fig1 = px.line(
        df,
        x="Round",
        y="Revenue",
        title="Revenue Trend"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    fig2 = px.line(
        df,
        x="Round",
        y="Stock Price",
        title="Stock Price Trend"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:

    st.info(
        "No simulation rounds completed yet."
    )

# =========================================================
# RESET BUTTON
# =========================================================

st.sidebar.header("Simulation Control")

if st.sidebar.button(
    "Reset Simulation"
):

    for key in list(
        st.session_state.keys()
    ):

        del st.session_state[key]

    st.rerun()
