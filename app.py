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

# Hold scenario
# -----
# 1) Original principal grows to current value
# 2) Tax applies only on gain portion at final sale
# 3) After-tax amount grows further

# Gain portion
hold_gain = current_value - purchase_price
after_tax_gain = hold_gain * (1 - tax_rate/100)
hold_net_value_now = purchase_price + after_tax_gain

# Future growth: after-tax base grows with new returns (assume no more tax for simplicity)
future_years = np.arange(2025, end_year + 1)
future_hold_value = [hold_net_value_now * ((1 + annual_return/100) ** (y - 2025)) for y in future_years]

# Combine
hold_value = np.linspace(purchase_price, current_value, 2025 - start_year + 1)
hold_net = np.concatenate((hold_value[:-1], [hold_net_value_now], future_hold_value))

# Sell & Rebuy scenario
# -----
# 1) Sell at sell_rebuy_year -> pay tax on gain since 2005
# 2) Rebuy with net proceeds
# 3) New basis grows with annual return
# 4) Final tax only on NEW gain since rebuy

# Gain portion at sell/rebuy
rebuy_gain = sell_rebuy_value - purchase_price
rebuy_after_tax = sell_rebuy_value - (rebuy_gain * tax_rate/100)

# Future growth
rebuy_future_years = np.arange(sell_rebuy_year, end_year + 1)
rebuy_gross = [rebuy_after_tax * ((1 + annual_return/100) ** (y - sell_rebuy_year)) for y in rebuy_future_years]

# Final tax on gain AFTER rebuy
rebuy_final_gain = rebuy_gross[-1] - rebuy_after_tax
rebuy_after_final_tax = rebuy_gross.copy()
rebuy_after_final_tax[-1] = rebuy_gross[-1] - (rebuy_final_gain * tax_rate/100)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(years, hold_value, label="Hold: Gross Value", linestyle="--", color="blue")
ax.plot(years, hold_net, label="Hold: After Tax & Growth", color="orange", linewidth=2)

ax.plot(rebuy_future_years, rebuy_gross, label="Sell & Rebuy: Gross Value", linestyle="--", color="green")
ax.plot(rebuy_future_years, rebuy_after_final_tax, label="Sell & Rebuy: After Tax & Growth", color="red", linewidth=2)

ax.axvline(sell_rebuy_year, color="gray", linestyle=":", label="Sell & Rebuy Year")
ax.axvline(2025, color="black", linestyle=":", label="Sell Year (Hold)")

ax.set_xlabel("Year")
ax.set_ylabel("Portfolio Value (€)")
ax.set_title("Hold vs. Sell & Rebuy: Smoothed & Corrected")
ax.legend()
ax.grid(True)

st.pyplot(fig)
