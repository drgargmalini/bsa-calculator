import streamlit as st
import math

st.title("🩺 Body Surface Area (BSA) Calculator")

height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
weight = st.number_input("Weight (kg)", min_value=10.0, max_value=300.0)

if st.button("Calculate BSA"):
    if height <= 0 or weight <= 0:
        st.error("Please enter valid height and weight values.")
    else:
        bsa = math.sqrt((height * weight) / 3600)

        st.markdown("### 📐 Calculated Body Surface Area")
        st.metric(
            label="BSA (Mosteller formula)",
            value=f"{bsa:.2f} m²"
        )

        st.info(
            "💡 **Clinical note:** BSA is commonly used for chemotherapy dosing, "
            "renal function estimation, and cardiac indexing."
        )


st.caption("Formula: Mosteller")








st.markdown("---")
st.caption(
    "⚠️ Disclaimer: This calculator is for educational purposes only. "
    "Clinical decisions should not be based solely on this tool. "
    "The developer is not responsible for clinical outcomes."
)

