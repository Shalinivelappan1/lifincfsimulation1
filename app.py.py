import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Corporate Finance Learning Lab",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "round" not in st.session_state:
    st.session_state.round = 1

if "cash" not in st.session_state:
    st.session_state.cash = 200.0

if "debt" not in st.session_state:
    st.session_state.debt = 150.0

if "equity" not in st.session_state:
    st.session_state.equity = 350.0

if "revenue" not in st.session_state:
    st.session_state.revenue = 500.0

if "profit" not in st.session_state:
    st.session_state.profit = 60.0

if "stock_price" not in st.session_state:
    st.session_state.stock_price = 100.0

if "wacc" not in st.session_state:
    st.session_state.wacc = 0.10

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------

def generate_macro_conditions():

    return {
        "GDP Growth": random.choice([3, 4, 5, 6, 7]),
        "Inflation": random.choice([3, 4, 5, 6, 7, 8]),
        "Interest Rate": random.choice([5, 6, 7, 8, 9]),
        "Market Sentiment": random.choice(
            ["Bullish", "Neutral", "Bearish"]
        )
    }


macro = generate_macro_conditions()


def calculate_wacc(debt, equity, interest_rate):

    total = debt + equity

    if total == 0:
        return 0.10

    rd = interest_rate / 100
    re = 0.14
    tax = 0.30

    wacc = (
        (equity / total) * re
        + (debt / total) * rd * (1 - tax)
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


def random_market_shock():

    shocks = [
        ("Interest Rate Hike", -5),
        ("Economic Boom", 10),
        ("Supply Chain Disruption", -8),
        ("Technology Breakthrough", 12),
        ("ESG Regulation", -3),
        ("Stable Economy", 2)
    ]

    return random.choice(shocks)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Corporate Finance Learning Lab")

st.markdown("""
This interactive learning lab helps students understand:

- Capital Budgeting
- Capital Structure
- Dividend Policy
- Working Capital Management
- Risk Management
- Firm Valuation

Students can experiment with financial decisions
and observe their impact on shareholder wealth.
""")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header("Simulation Status")

st.sidebar.metric(
    "Round",
    st.session_state.round
)

st.sidebar.header("Macroeconomic Conditions")

for key, value in macro.items():
    st.sidebar.write(f"**{key}:** {value}")

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

st.header("Company Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Cash",
    f"₹ {round(st.session_state.cash,2)} Cr"
)

col2.metric(
    "Debt",
    f"₹ {round(st.session_state.debt,2)} Cr"
)

col3.metric(
    "Profit",
    f"₹ {round(st.session_state.profit,2)} Cr"
)

col4.metric(
    "Stock Price",
    f"₹ {round(st.session_state.stock_price,2)}"
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

(
    overview_tab,
    investment_tab,
    capital_structure_tab,
    dividend_tab,
    working_capital_tab,
    risk_tab,
    valuation_tab,
    results_tab
) = st.tabs([
    "Financial Health Overview",
    "Capital Budgeting Learning Lab",
    "Capital Structure Learning Lab",
    "Dividend Policy Learning Lab",
    "Working Capital Learning Lab",
    "Risk Management Learning Lab",
    "Firm Valuation Learning Lab",
    "Strategic Reflection Dashboard"
])

# ---------------------------------------------------
# OVERVIEW TAB
# ---------------------------------------------------

with overview_tab:

    st.subheader("Financial Health Overview")

    de_ratio = (
        st.session_state.debt /
        st.session_state.equity
    )

    current_ratio = (
        (st.session_state.cash + 100) / 80
    )

    overview1, overview2, overview3 = st.columns(3)

    overview1.metric(
        "Debt-to-Equity Ratio",
        round(de_ratio, 2)
    )

    overview2.metric(
        "Current Ratio",
        round(current_ratio, 2)
    )

    overview3.metric(
        "WACC",
        f"{round(st.session_state.wacc*100,2)}%"
    )

    st.info("""
    This dashboard summarizes:
    - liquidity,
    - leverage,
    - financing cost,
    - and financial stability.
    """)

# ---------------------------------------------------
# CAPITAL BUDGETING TAB
# ---------------------------------------------------

with investment_tab:

    st.subheader("Concept Learning: Capital Budgeting")

    st.latex(
        r'''NPV = \sum_{t=1}^{n}\frac{CF_t}{(1+r)^t} - C_0'''
    )

    st.latex(
        r'''PI = \frac{PV\ of\ Future\ Cash\ Flows}{Initial\ Investment}'''
    )

    st.latex(
        r'''Payback\ Period = \frac{Initial\ Investment}{Annual\ Cash\ Inflow}'''
    )

    with st.expander("Learn About Capital Budgeting"):
        st.write("""
        Capital budgeting evaluates long-term investment decisions.
        Positive NPV projects create shareholder value.
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

    npv = calculate_npv(
        investment_amount,
        expected_cashflow,
        discount_rate / 100
    )

    payback_period = round(
        investment_amount / expected_cashflow,
        2
    )

    profitability_index = round(
        (npv + investment_amount) /
        investment_amount,
        2
    )

    cap1, cap2, cap3 = st.columns(3)

    cap1.metric("NPV", f"₹ {npv} Cr")
    cap2.metric("Payback Period", payback_period)
    cap3.metric("Profitability Index", profitability_index)

    if npv > 0:
        st.success(
            "The project is expected to create shareholder value."
        )
    else:
        st.error(
            "The project may destroy shareholder value."
        )

# ---------------------------------------------------
# CAPITAL STRUCTURE TAB
# ---------------------------------------------------

with capital_structure_tab:

    st.subheader("Concept Learning: Capital Structure")

    st.latex(
        r'''WACC = \frac{E}{V}R_e + \frac{D}{V}R_d(1-T)'''
    )

    st.latex(
        r'''Debt\text{-}to\text{-}Equity = \frac{Debt}{Equity}'''
    )

    with st.expander("Learn About Capital Structure"):
        st.write("""
        Capital structure refers to the mix of debt and equity financing.
        Moderate leverage may reduce WACC,
        but excessive leverage increases financial distress risk.
        """)

    debt_financing = st.slider(
        "New Debt Raised (₹ Cr)",
        0,
        200,
        20
    )

    equity_financing = st.slider(
        "New Equity Issued (₹ Cr)",
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

    projected_de_ratio = round(
        projected_debt /
        projected_equity,
        2
    )

    interest_coverage = round(
        st.session_state.profit /
        max(1, projected_debt * 0.08),
        2
    )

    cs1, cs2, cs3 = st.columns(3)

    cs1.metric(
        "Projected WACC",
        f"{round(projected_wacc*100,2)}%"
    )

    cs2.metric(
        "Debt-to-Equity",
        projected_de_ratio
    )

    cs3.metric(
        "Interest Coverage",
        interest_coverage
    )

    if projected_de_ratio > 1.5:
        st.error(
            "The firm may be approaching financial distress."
        )

# ---------------------------------------------------
# DIVIDEND TAB
# ---------------------------------------------------

with dividend_tab:

    st.subheader("Concept Learning: Dividend Policy")

    st.latex(
        r'''Dividend\ Payout\ Ratio = \frac{Dividends}{Net\ Income}'''
    )

    st.latex(
        r'''Dividend\ Yield = \frac{Dividend\ Per\ Share}{Stock\ Price}'''
    )

    with st.expander("Learn About Dividend Policy"):
        st.write("""
        Dividend policy influences:
        - shareholder expectations,
        - growth opportunities,
        - and market signaling.
        """)

    dividend_policy = st.selectbox(
        "Select Dividend Policy",
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
        st.warning(
            "High dividends may reduce future growth flexibility."
        )

    elif dividend_policy == "No Dividend":
        st.info(
            "Retaining earnings may support future investments."
        )

    elif dividend_policy == "Share Buyback":
        st.success(
            "Share buybacks may improve EPS and investor confidence."
        )

# ---------------------------------------------------
# WORKING CAPITAL TAB
# ---------------------------------------------------

with working_capital_tab:

    st.subheader(
        "Concept Learning: Working Capital Management"
    )

    st.latex(
        r'''CCC = DIO + DSO - DPO'''
    )

    with st.expander(
        "Learn About Cash Conversion Cycle"
    ):
        st.write("""
        Cash Conversion Cycle measures
        how efficiently the company converts
        operations into cash.
        """)

    credit_policy = st.selectbox(
        "Credit Policy",
        ["Strict", "Moderate", "Liberal"]
    )

    inventory_policy = st.selectbox(
        "Inventory Policy",
        ["Low", "Medium", "High"]
    )

    supplier_payment = st.selectbox(
        "Supplier Payment Strategy",
        ["Early", "Standard", "Delayed"]
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

    wc1, wc2 = st.columns(2)

    wc1.metric(
        "Cash Conversion Cycle",
        f"{ccc} Days"
    )

    wc2.metric(
        "Current Ratio",
        round(current_ratio, 2)
    )

# ---------------------------------------------------
# RISK MANAGEMENT TAB
# ---------------------------------------------------

with risk_tab:

    st.subheader("Concept Learning: Risk Management")

    hedge_policy = st.selectbox(
        "Hedging Strategy",
        [
            "No Hedging",
            "Partial Hedging",
            "Full Hedging"
        ]
    )

    risk_exposure = random.choice(
        [
            "Interest Rate Risk",
            "FX Risk",
            "Commodity Risk",
            "Liquidity Risk"
        ]
    )

    st.metric(
        "Current Major Risk",
        risk_exposure
    )

    if hedge_policy == "No Hedging":
        st.warning(
            "The company remains fully exposed to market volatility."
        )

    elif hedge_policy == "Partial Hedging":
        st.info(
            "The company partially reduces financial uncertainty."
        )

    else:
        st.success(
            "The company significantly reduces financial risk exposure."
        )

# ---------------------------------------------------
# VALUATION TAB
# ---------------------------------------------------

with valuation_tab:

    st.subheader("Concept Learning: Firm Valuation")

    st.latex(
        r'''Firm\ Value = \sum_{t=1}^{n}\frac{FCFF_t}{(1+WACC)^t}'''
    )

    with st.expander("Learn About Firm Valuation"):
        st.write("""
        Firm valuation estimates
        the intrinsic value of a company
        based on future cash flows.
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

# ---------------------------------------------------
# RUN SIMULATION
# ---------------------------------------------------

st.header("Run Simulation")

if st.button("Run Simulation Round"):

    shock_name, shock_effect = random_market_shock()

    revenue_growth = np.random.uniform(0.02, 0.15)

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
        st.session_state.stock_price
        + (updated_profit / 10)
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

    if updated_cash < 20:
        st.error(
            "Liquidity stress detected."
        )

    elif projected_de_ratio > 1.5:
        st.warning(
            "Leverage risk is increasing."
        )

    else:
        st.success(
            "The company maintains reasonable financial stability."
        )

# ---------------------------------------------------
# RESULTS TAB
# ---------------------------------------------------

with results_tab:

    st.subheader("Strategic Reflection Dashboard")

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

# ---------------------------------------------------
# RESET BUTTON
# ---------------------------------------------------

if st.sidebar.button("Reset Simulation"):

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()
