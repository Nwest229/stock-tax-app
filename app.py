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

# Timeline setup
start_year = 2005
sell_year_hold = 2025
end_year = sell_year_hold + years_to_future

years_hold = np.arange(start_year, end_year + 1)
years_rebuy = np.arange(sell_rebuy_year, end_year + 1)

# ------------------------------
# 📌 Hold scenario
# ------------------------------

# 1) Before sell
hold_years_before_sell = np.arange(start_year, sell_year_hold + 1)
hold_value_before = np.linspace(purchase_price, current_value, len(hold_years_before_sell))

# 2) Final tax at sell
hold_gain = current_value - purchase_price
after_tax_gain = hold_gain * (1 - tax_rate/100)
hold_net_value_now = purchase_price + after_tax_gain

# 3) Future growth after sell
hold_years_after_sell = np.arange(sell_year_hold + 1, end_year + 1)
hold_value_after = [hold_net_value_now * ((1 + annual_return/100) ** (y - sell_year_hold)) for y in hold_years_after_sell]

# 4) Inflation-adjusted
hold_value_after_real = [
    v / ((1 + annual_inflation/100) ** (y - sell_year_hold)) for v, y in zip(hold_value_after, hold_years_after_sell)
]

# 5) Combine
hold_net = np.concatenate((hold_value_before, hold_value_after))
hold_net_real = np.concatenate((hold_value_before, hold_value_after_real))

# ------------------------------
# 📌 Sell & Rebuy scenario
# ------------------------------

# 1) Sell & pay tax
rebuy_gain = sell_rebuy_value - purchase_price
rebuy_after_tax = sell_rebuy_value - (rebuy_gain * tax_rate/100)

# 2) Future growth
rebuy_future = [rebuy_after_tax * ((1 + annual_return/100) ** (y - sell_rebuy_year)) for y in years_rebuy]

# 3) Final tax only on new gain since rebuy
rebuy_final_gain = rebuy_future[-1] - rebuy_after_tax
rebuy_after_final_tax = rebuy_future.copy()
rebuy_after_final_tax[-1] = rebuy_future[-1] - (rebuy_final_gain * tax_rate/100)

# 4) Inflation-adjusted
rebuy_after_final_tax_real = [
    v / ((1 + annual_inflation/100) ** (y - sell_year_hold)) for v, y in zip(rebuy_after_final_tax, years_rebuy)
]

# ------------------------------
# ✅ Plot
# ------------------------------

fig, ax = plt.subplots(figsize=(12, 6))

# Hold
ax.plot(years_hold, hold_net, label="Hold: After Tax & Growth", color="orange", linewidth=2)
ax.plot(years_hold, hold_net_real, label="Hold: After Tax & Inflation", color="orange", linestyle=':')

# Rebuy
ax.plot(years_rebuy, rebuy_after_final_tax, label="Sell & Rebuy: After Tax & Growth", color="red", linewidth=2)
ax.plot(years_rebuy, rebuy_after_final_tax_real, label="Sell & Rebuy: After Tax & Inflation", color="red", linestyle=':')

# Markers
ax.axvline(sell_rebuy_year, color="gray", linestyle=":", label="Sell & Rebuy Year")
ax.axvline(sell_year_hold, color="black", linestyle=":", label="Sell Year (Hold)")

# Labels
ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value (€)")
ax.set_title("Hold vs. Sell & Rebuy: Inflation-Adjusted Comparison")
ax.legend()
ax.grid(True)

st.pyplot(fig)
