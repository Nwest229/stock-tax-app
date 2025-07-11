import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Hold vs. Sell & Rebuy: Inherited Stocks in Germany")

st.sidebar.header("Your Scenario Inputs")

# Inputs
purchase_price = st.sidebar.number_input("Original Purchase Price (€)", value=10000)
current_value = st.sidebar.number_input("Current Value (€)", value=50000)
sell_rebuy_year = st.sidebar.slider("Year of Hypothetical Sell & Rebuy", 2005, 2025, 2015)
sell_rebuy_value = st.sidebar.number_input("Value when Sold & Rebuy (€)", value=40000)
tax_rate = st.sidebar.slider("Effective Tax Rate (%)", 0.0, 50.0, 26.375)
annual_return = st.sidebar.slider("Annual Return After Rebuy (%)", 0.0, 20.0, 5.0)
annual_inflation = st.sidebar.slider("Annual Inflation Rate (%)", 0.0, 10.0, 2.0)
years_to_future = st.sidebar.slider("Years into the Future", 0, 20, 5)

# Timeline
start_year = 2005
sell_year_hold = 2025
end_year = sell_year_hold + years_to_future

years_hold = np.arange(start_year, end_year + 1)
years_rebuy = np.arange(sell_rebuy_year, end_year + 1)

# Hold: split timeline
hold_years_before_sell = np.arange(start_year, sell_year_hold + 1)
hold_years_after_sell = np.arange(sell_year_hold + 1, end_year + 1)

# Hold gross value before sell
hold_value_before = np.linspace(purchase_price, current_value, len(hold_years_before_sell))

# Hold future growth AFTER tax
hold_gain = current_value - purchase_price
after_tax_gain = hold_gain * (1 - tax_rate/100)
hold_net_value_now = purchase_price + after_tax_gain

hold_value_after = [hold_net_value_now * ((1 + annual_return/100) ** (y - sell_year_hold)) for y in hold_years_after_sell]

# Real adjustment
hold_value_after_real = [
    v / ((1 + annual_inflation/100) ** (y - sell_year_hold)) for v, y in zip(hold_value_after, hold_years_after_sell)
]

# Merge
hold_net = np.concatenate((hold_value_before, hold_value_after))
hold_net_real = np.concatenate((hold_value_before, hold_value_after_real))

# Combine
hold_value = np.linspace(purchase_price, current_value, 2025 - start_year + 1)
hold_net = np.concatenate((hold_value[:-1], [hold_net_value_now], future_hold_value))
hold_net_real = np.concatenate((hold_value[:-1], [hold_net_value_now], future_hold_value_real))

# Sell & Rebuy scenario
rebuy_gain = sell_rebuy_value - purchase_price
rebuy_after_tax = sell_rebuy_value - (rebuy_gain * tax_rate/100)

rebuy_future_years = np.arange(sell_rebuy_year, end_year + 1)
rebuy_gross = [rebuy_after_tax * ((1 + annual_return/100) ** (y - sell_rebuy_year)) for y in rebuy_future_years]

rebuy_final_gain = rebuy_gross[-1] - rebuy_after_tax
rebuy_after_final_tax = rebuy_gross.copy()
rebuy_after_final_tax[-1] = rebuy_gross[-1] - (rebuy_final_gain * tax_rate/100)

rebuy_after_final_tax_real = [
    v / ((1 + annual_inflation/100) ** (y - 2025)) for v, y in zip(rebuy_after_final_tax, rebuy_future_years)
]

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(years, hold_value, label="Hold: Gross Value", linestyle="--", color="blue")
ax.plot(years, hold_net, label="Hold: After Tax & Growth", color="orange", linewidth=2)
ax.plot(years, hold_net_real, label="Hold: After Tax & Inflation", color="orange", linewidth=2, linestyle=':')

ax.plot(rebuy_future_years, rebuy_gross, label="Sell & Rebuy: Gross Value", linestyle="--", color="green")
ax.plot(rebuy_future_years, rebuy_after_final_tax, label="Sell & Rebuy: After Tax & Growth", color="red", linewidth=2)
ax.plot(rebuy_future_years, rebuy_after_final_tax_real, label="Sell & Rebuy: After Tax & Inflation", color="red", linewidth=2, linestyle=':')

ax.axvline(sell_rebuy_year, color="gray", linestyle=":", label="Sell & Rebuy Year")
ax.axvline(2025, color="black", linestyle=":", label="Sell Year (Hold)")

ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value (€)")
ax.set_title("Hold vs. Sell & Rebuy: Inflation-Adjusted Comparison")
ax.legend()
ax.grid(True)

st.pyplot(fig)
