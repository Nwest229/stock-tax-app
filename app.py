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
years_to_future = st.sidebar.slider("Years into the Future", 0, 20, 5)

# Timeline
start_year = 2005
end_year = 2025 + years_to_future
years = np.arange(start_year, end_year + 1)

# Scenario 1: Hold
hold_value = np.linspace(purchase_price, current_value, 2025 - start_year + 1)
hold_future_years = np.arange(2026, end_year + 1)
future_hold = [current_value * ((1 + annual_return/100) ** (y - 2025)) for y in hold_future_years]
hold_value = np.concatenate((hold_value, future_hold))

# Net value after final tax
hold_net = hold_value.copy()
hold_net[years >= 2025] = hold_value[years >= 2025] * (1 - tax_rate/100)

# Scenario 2: Sell & Rebuy
sell_idx = sell_rebuy_year - start_year
rebuy_value = sell_rebuy_value * (1 - tax_rate/100)
rebuy_future_years = np.arange(sell_rebuy_year, end_year + 1)
rebuy_curve = [rebuy_value * ((1 + annual_return/100) ** (y - sell_rebuy_year)) for y in rebuy_future_years]

# Final tax when selling rebought shares
rebuy_net = np.array(rebuy_curve)
rebuy_net[-1] = rebuy_net[-1] * (1 - tax_rate/100)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(years, hold_value, label="Hold: Gross Value", linestyle="--")
ax.plot(years, hold_net, label="Hold: After Tax", linewidth=2)
ax.plot(rebuy_future_years, rebuy_curve, label="Sell & Rebuy: Gross Value", linestyle="--")
ax.plot(rebuy_future_years, rebuy_net, label="Sell & Rebuy: After Tax", linewidth=2)

ax.axvline(sell_rebuy_year, color="gray", linestyle=":", label="Sell & Rebuy Year")
ax.axvline(2025, color="black", linestyle=":", label="Sell Year (Hold)")

ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value (€)")
ax.set_title("Hold vs. Sell & Rebuy Comparison")
ax.legend()
ax.grid(True)

st.pyplot(fig)
