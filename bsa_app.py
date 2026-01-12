import streamlit as st
import math

st.set_page_config(page_title="BSA & BMI Calculator", page_icon="🩺")

st.title("🩺 BSA & BMI Calculator")

# ---- Patient Type Toggle ----
patient_type = st.radio(
    "Select patient type",
    ["Adult", "Pediatric"],
    horizontal=True
)

st.markdown("---")

# ---- Inputs ----
height = st.number_input(
    "Height (cm)",
    min_value=30.0 if patient_type == "Pediatric" else 50.0,
    max_value=200.0 if patient_type == "Pediatric" else 250.0,
    step=0.5
)

weight = st.number_input(
    "Weight (kg)",
    min_value=2.0 if patient_type == "Pediatric" else 10.0,
    max_value=100.0 if patient_type == "Pediatric" else 300.0,
    step=0.1
)

# ---- Calculate Button ----
if st.button("Calculate"):
    if height <= 0 or weight <= 0:
        st.error("Please enter valid height and weight.")
    else:
        # ---- BSA (Mosteller) ----
        bsa = math.sqrt((height * weight) / 3600)

        # ---- BMI ----
        height_m = height / 100
        bmi = weight / (height_m ** 2)

        st.markdown("## 📊 Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Body Surface Area (BSA)",
                value=f"{bsa:.2f} m²"
            )

        with col2:
            st.metric(
                label="Body Mass Index (BMI)",
                value=f"{bmi:.1f} kg/m²"
            )

        # ---- BMI Interpretation (Adults only) ----
        if patient_type == "Adult":
            if bmi < 18.5:
                bmi_status = "Underweight"
            elif 18.5 <= bmi < 25:
                bmi_status = "Normal weight"
            elif 25 <= bmi < 30:
                bmi_status = "Overweight"
            else:
                bmi_status = "Obese"

            st.info(f"📌 **BMI Category (Adult):** {bmi_status}")

        else:
            st.warning(
                "📌 **Note:** Pediatric BMI interpretation depends on age- and sex-specific percentiles."
            )

# ---- Disclaimer ----
st.markdown("---")
st.caption(
    "⚠️ Disclaimer: This calculator is for educational purposes only. "
    "Clinical decisions should not be based solely on this tool. "
    "The developer is not responsible for clinical outcomes."
)

