import streamlit as st
import math

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="BSA & BMI Calculator",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 BSA & BMI Calculator")

# -------------------------------------------------
# Patient type
# -------------------------------------------------
patient_type = st.radio(
    "Select patient type",
    ["Adult", "Pediatric"],
    horizontal=True
)

st.markdown("---")

# -------------------------------------------------
# Pediatric-specific inputs
# -------------------------------------------------
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

# -------------------------------------------------
# Adult sex input (needed for IBW)
# -------------------------------------------------
if patient_type == "Adult":
    sex = st.selectbox("Sex", ["Male", "Female"])

# -------------------------------------------------
# Common inputs
# -------------------------------------------------
height = st.number_input(
    "Height (cm)",
    min_value=30.0 if patient_type == "Pediatric" else 50.0,
    max_value=200.0 if patient_type == "Pediatric" else 250.0,
    step=0.5
)

weight = st.number_input(
    "Actual Body Weight (kg)",
    min_value=2.0 if patient_type == "Pediatric" else 10.0,
    max_value=100.0 if patient_type == "Pediatric" else 300.0,
    step=0.1
)

# -------------------------------------------------
# Calculate
# -------------------------------------------------
if st.button("Calculate"):
    if height <= 0 or weight <= 0:
        st.error("Please enter valid height and weight values.")
    else:
        height_m = height / 100

        # Actual BMI & BSA
        actual_bmi = weight / (height_m ** 2)
        actual_bsa = math.sqrt((height * weight) / 3600)

        st.markdown("## 📊 Results")

        # -------------------------------------------------
        # ADULT LOGIC
        # -------------------------------------------------
        if patient_type == "Adult":

            # Ideal Body Weight (Devine)
            if sex == "Male":
                ibw = 50 + 0.9 * (height - 152)
            else:
                ibw = 45.5 + 0.9 * (height - 152)

            ibw = max(ibw, 0)

            ideal_bmi = ibw / (height_m ** 2)
            ideal_bsa = math.sqrt((height * ibw) / 3600)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🔹 Actual")
                st.metric("Weight", f"{weight:.1f} kg")
                st.metric("BMI", f"{actual_bmi:.1f} kg/m²")
                st.metric("BSA", f"{actual_bsa:.2f} m²")

            with col2:
                st.markdown("### 🔹 Ideal (IBW-based)")
                st.metric("Ideal Body Weight", f"{ibw:.1f} kg")
                st.metric("Ideal BMI", f"{ideal_bmi:.1f} kg/m²")
                st.metric("Ideal BSA", f"{ideal_bsa:.2f} m²")

            # BMI interpretation (Adult)
            st.markdown("### 📌 BMI Interpretation (Adult)")

            if actual_bmi < 18.5:
                status = "Underweight"
                color = "🔵"
                ref = "< 18.5"
            elif 18.5 <= actual_bmi < 25:
                status = "Normal"
                color = "🟢"
                ref = "18.5 – 24.9"
            elif 25 <= actual_bmi < 30:
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

            st.info(
                "🧠 **Clinical note:** Ideal Body Weight (Devine formula) is commonly used "
                "for dose calculations in obese or underweight adults. "
                "Clinical judgement is essential."
            )

        # -------------------------------------------------
        # PEDIATRIC LOGIC
        # -------------------------------------------------
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Actual Weight", f"{weight:.1f} kg")

            with col2:
                st.metric("BMI", f"{actual_bmi:.1f} kg/m²")

            st.metric("BSA", f"{actual_bsa:.2f} m²")

            if age_years < 2:
                st.warning(
                    "📌 **Pediatric note:** BMI is not recommended for children under 2 years. "
                    "Use weight-for-length charts instead."
                )
            else:
                # Approximate percentile categories
                if actual_bmi < 14:
                    p_status = "Underweight (<5th percentile)"
                    color = "🔵"
                elif 14 <= actual_bmi < 17:
                    p_status = "Healthy weight (5th–85th percentile)"
                    color = "🟢"
                elif 17 <= actual_bmi < 19:
                    p_status = "Overweight (85th–95th percentile)"
                    color = "🟠"
                else:
                    p_status = "Obese (≥95th percentile)"
                    color = "🔴"

                st.markdown(
                    f"{color} **Pediatric BMI Category:** {p_status}"
                )

                st.info(
                    "📘 **Reference:** Pediatric BMI interpretation is based on "
                    "CDC age- and sex-specific percentile charts (2–18 years). "
                    "This tool provides an approximate classification."
                )

        # -------------------------------------------------
        # BSA clinical note (common)
        # -------------------------------------------------
        st.info(
            "🧠 **Clinical note (BSA):** BSA is used for chemotherapy dosing, "
            "cardiac index calculation, renal function normalization, "
            "and physiological indexing."
        )

# -------------------------------------------------
# Branding
# -------------------------------------------------
st.markdown("---")
st.markdown(
    """
    **Developed by**  
    🩺 **Dr Malini Avinash Gupta**  
    """
)

# -------------------------------------------------
# Disclaimer
# -------------------------------------------------
st.caption(
    "⚠️ Disclaimer: This calculator is for educational purposes only. "
    "Clinical decisions should not be based solely on this tool. "
    "The developer is not responsible for clinical outcomes."
)

