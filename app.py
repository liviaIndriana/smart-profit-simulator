import streamlit as st
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Smart Profit Simulator",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

.big-title {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    color: #f8fafc;
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 2px solid #334155;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    color: #cbd5e1;
}

.card {
    background-color: #f8fafc;
    color: #0f172a;
    padding: 25px;
    border-radius: 14px;
    border: 3px solid #334155;
    box-shadow: 6px 6px 0px #1e293b;
}

.card-title {
    font-size: 15px;
    font-weight: 800;
    color: #475569;
}

.card-value {
    font-size: 32px;
    font-weight: 900;
    color: #2563eb;
}

.badge {
    background-color: #dcfce7;
    color: #166534;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}

.warning-badge {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 10px;
    border-radius: 8px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# MODEL
X_train = np.array([
    [5, 10],
    [10, 20],
    [15, 5],
    [20, 25],
    [25, 15]
])

y_train = np.array([
    50,
    80,
    110,
    90,
    150
])

model = LinearRegression()
model.fit(X_train, y_train)

baseline_input = np.array([[10, 10]])
baseline_profit = model.predict(baseline_input)[0]

# HEADER
st.markdown('<div class="big-title"> DASHBOARD SIMULASI KEUNTUNGAN</div>', unsafe_allow_html=True)

st.write("")

# SIDEBAR
# DEFAULT VALUE
if "advertising" not in st.session_state:
    st.session_state.advertising = 10

if "discount" not in st.session_state:
    st.session_state.discount = 10

# FUNCTION RESET
def reset_baseline():
    st.session_state.advertising = 10
    st.session_state.discount = 10

# SIDEBAR
st.sidebar.info("Atur strategi iklan dan diskon untuk melihat dampaknya terhadap keuntungan.")

st.sidebar.markdown("### 📢 Biaya Iklan")
advertising = st.sidebar.slider(
    "Geser untuk mengatur biaya iklan",
    min_value=0,
    max_value=50,
    step=1,
    key="advertising"
)

st.sidebar.markdown("### 🏷️ Diskon Produk")
discount = st.sidebar.slider(
    "Geser untuk mengatur persentase diskon",
    min_value=0,
    max_value=50,
    step=1,
    key="discount"
)

st.sidebar.markdown("---")

st.sidebar.markdown(f"""
### 📌 Skenario Aktif
**Iklan:** Rp {advertising} Juta  
**Diskon:** {discount}%  
""")

st.sidebar.button(
    "🔄 Kembali ke Baseline",
    on_click=reset_baseline
)

# PREDICTION
input_data = np.array([[advertising, discount]])
prediction = model.predict(input_data)[0]
delta = prediction - baseline_profit
percentage_change = (delta / baseline_profit) * 100

# KPI CARDS
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">SKENARIO BARU</div>
        <div class="card-value">Rp {prediction:.2f} Juta</div>
        <br>
        <b>Iklan:</b> {advertising} Juta<br>
        <b>Diskon:</b> {discount}%
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">BASELINE</div>
        <div class="card-value">Rp {baseline_profit:.2f} Juta</div>
        <br>
        <b>Iklan:</b> 10 Juta<br>
        <b>Diskon:</b> 10%
    </div>
    """, unsafe_allow_html=True)

with col3:
    badge_class = "badge" if delta >= 0 else "warning-badge"
    status = "RECOMMENDED" if delta >= 0 else "REVIEW STRATEGY"

    st.markdown(f"""
    <div class="card">
        <div class="card-title">DAMPAK PROFIT</div>
        <div class="card-value">Rp {delta:+.2f} Juta</div>
        <br>
        <div class="{badge_class}">
            {percentage_change:+.2f}% dibanding baseline<br>
            {status}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# CHART
left, right = st.columns([2, 1])

with left:
    st.subheader("📊 Perbandingan Profit")

    chart_data = pd.DataFrame({
        "Scenario": ["Baseline", "Simulation"],
        "Profit": [baseline_profit, prediction]
    })

    st.bar_chart(chart_data, x="Scenario", y="Profit", use_container_width=True)

with right:
    st.subheader("📈 Performance Score")

    progress_value = int(min(max((prediction / 150) * 100, 0), 100))
    st.progress(progress_value)
    st.metric("Score", f"{progress_value}%")

    if progress_value >= 80:
        st.success("Performa sangat baik")
    elif progress_value >= 50:
        st.info("Performa cukup baik")
    else:
        st.warning("Performa perlu ditingkatkan")

st.divider()

# RECOMMENDATION
st.subheader("💡 Rekomendasi Bisnis")

if delta >= 20:
    st.success("""
### Strategi Sangat Baik
Skenario ini diprediksi meningkatkan keuntungan secara signifikan.

**Rekomendasi:**
- Tingkatkan biaya iklan secara bertahap
- Jaga diskon agar tidak terlalu tinggi
- Cocok untuk kampanye promosi besar
""")

elif delta >= 0:
    st.info("""
### Strategi Cukup Baik
Skenario ini masih memberikan peningkatan keuntungan.

**Rekomendasi:**
- Strategi dapat dilanjutkan
- Pantau respon pelanggan
- Evaluasi hasil secara berkala
""")

else:
    st.warning("""
### Strategi Perlu Ditinjau
Skenario ini berpotensi menurunkan keuntungan.

**Rekomendasi:**
- Kurangi persentase diskon
- Atur ulang biaya iklan
- Coba kombinasi skenario lain
""")

st.divider()

# MODEL INSIGHT
st.subheader("🧠 Wawasan Model")

coef = model.coef_
intercept = model.intercept_

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
### Persamaan Regresi

Profit = {intercept:.2f} + ({coef[0]:.2f} × Iklan) + ({coef[1]:.2f} × Diskon)

Artinya:
- Setiap kenaikan iklan 1 juta memengaruhi profit sebesar {coef[0]:.2f} juta
- Setiap kenaikan diskon 1% memengaruhi profit sebesar {coef[1]:.2f} juta
""")

with col2:
    sensitivity_iklan = abs(coef[0] * 5)
    sensitivity_diskon = abs(coef[1] * 5)

    if sensitivity_iklan > sensitivity_diskon:
        sensitive_var = "Biaya Iklan"
    else:
        sensitive_var = "Diskon"

    st.success(f"""
### Analisis Sensitivitas

Jika variabel dinaikkan 5 unit:

- Dampak Iklan: {sensitivity_iklan:.2f} juta
- Dampak Diskon: {sensitivity_diskon:.2f} juta

Variabel paling sensitif: **{sensitive_var}**
""")

st.divider()

# SUMMARY
st.subheader("📋 Ringkasan Simulasi")

summary = pd.DataFrame({
    "Variabel": [
        "Biaya Iklan",
        "Diskon",
        "Baseline Profit",
        "Predicted Profit",
        "Selisih Profit",
        "Status Keputusan"
    ],
    "Nilai": [
        f"{advertising} Juta",
        f"{discount}%",
        f"{baseline_profit:.2f} Juta",
        f"{prediction:.2f} Juta",
        f"{delta:.2f} Juta",
        "Recommended" if delta >= 0 else "Review Again"
    ]
})

st.dataframe(summary, use_container_width=True, hide_index=True)

st.divider()

with st.expander("Tentang Simulator"):
    st.write("""
Aplikasi ini menggunakan Linear Regression untuk melakukan simulasi What-If Analysis.

Pengguna dapat mengubah:
- Biaya Iklan
- Persentase Diskon

Kemudian aplikasi akan memprediksi perubahan keuntungan dibandingkan kondisi baseline.
""")

st.caption("📊 Smart Profit Simulator | Created by Livia Indriana Sari © 2026")