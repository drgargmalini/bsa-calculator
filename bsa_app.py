import streamlit as st
import math

st.title("🩺 Body Surface Area (BSA) Calculator")

height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0)

if st.button("Calculate BSA"):
    bsa = math.sqrt((height * weight) / 3600)
    st.success(f"BSA: {bsa:.2f} m²")

st.caption("Formula: Mosteller")
