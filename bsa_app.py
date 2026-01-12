import streamlit as st
import math

st.set_page_config(page_title="BSA & BMI Calculator", page_icon="🩺")

st.title("🩺 BSA & BMI Calculator")

# ---- Patient Type ----
patient_type = st.radio(
    "Select patient type",
    ["Adult", "Pediatric"],
    horizontal=True
)

st.markdown("---")

# ---- Pediatric-specific inputs ----
if patient_type == "Pediatric":
    col_age, col_sex = st.columns(2)

    with col_age:
        age_years = st.number_input(
            "Age (years)",
            min_value=0.0,
            max_value=18.0,
            step=0.1
        )

    with col_sex:
        sex = st.selectbox("Sex", ["Male", "Female"])

# ---- Common inputs ----
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

# ---- Calculate ----
if st.button("Calculate"):
    if height <= 0 or weight <= 0:
        st.error("Please enter valid height and weight values.")
    else:
        # ---- Calculations ----
        bsa = math.sqrt((height * weight) / 3600)
        height_m = height / 100
        bmi = weight / (height_m ** 2)

        st.markdown("## 📊 Results")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Body Surface Area (BSA)", f"{bsa:.2f} m²")

        with col2:
            st.metric("Body Mass Index (BMI)", f"{bmi:.1f} kg/m²")

        # ---- Clinical note for BSA ----
        st.info(
            "🧠 **Clinical note (BSA):** Used for chemotherapy dosing, cardiac index "
            "calculation, renal function normalization, and physiological indexing."
        )

        # ---- BMI Interpretation ----
        st.markdown("### 📌 BMI Interpretation")

        # ---------- ADULT ----------
        if patient_type == "Adult":
            if bmi < 18.5:
                status = "Underweight"
                color = "🔵"
                ref = "< 18.5"
            elif 18.5 <= bmi < 25:
                status = "Normal"
                color = "🟢"
                ref = "18.5 – 24.9"
            elif 25 <= bmi < 30:
                status = "Overweight"
                color = "🟠"
                ref = "25.0 – 29.9"
            else:
                status = "Obese"
                color = "🔴"
                ref = "≥ 30.0"

            st.markdown(
                f"""
                {color} **Category:** {status}  
                📏 **Reference range:** {ref} kg/m²
                """
            )

            st.markdown(
                """
                **Adult BMI reference (WHO):**
                - Normal: 18.5 – 24.9  
                - Overweight: 25.0 – 29.9  
                - Obesity: ≥ 30.0
                """
            )

        # ---------- PEDIATRIC ----------
        else:
            if age_years < 2:
                st.warning(
                    "📌 **Note:** BMI is not recommended for children under 2 years. "
                    "Use weight-for-length charts instead."
                )
            else:
                # Simplified CDC percentile-based classification
                if bmi < 14:
                    p_status = "Underweight (<5th percentile)"
                    color = "🔵"
                elif 14 <= bmi < 17:
                    p_status = "Healthy weight (5th–85th percentile)"
                    color = "🟢"
                elif 17 <= bmi < 19:
                    p_status = "Overweight (85th–95th percentile)"
                    color = "🟠"
                else:
                    p_status = "Obese (≥95th percentile)"
                    color = "🔴"

                st.markdown(
                    f"""
                    {color} **Pediatric BMI Category:** {p_status}
                    """
                )

                st.info(
                    "📘 **Reference:** Pediatric BMI interpretation is based on "
                    "CDC age- and sex-specific percentile charts (2–18 years). "
                    "This tool provides an approximate classification; "
                    "formal assessment should use validated growth charts."
                )

st.markdown("---")

st.markdown(
    """
    **Developed by**  
    🩺 **Dr Malini Avinash Gupta**   
    """
)


# ---- Disclaimer ----
st.markdown("---")
st.caption(
    "⚠️ Disclaimer: This calculator is for educational purposes only. "
    "Clinical decisions should not be based solely on this tool. "
    "The developer is not responsible for clinical outcomes."
)


