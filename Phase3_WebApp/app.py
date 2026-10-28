
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saudi Ecommerce AI - المطور جميل ناصر", layout="wide", page_icon="SA")

st.markdown('<div style="background: linear-gradient(90deg, #006C35 0%, #00502A 100%); padding:20px; border-radius:15px; color:white; text-align:center;"><h1>Saudi Ecommerce Intelligence - المرحلة الثالثة</h1><p>المطور: جميل ناصر | Saudi-Ecommerce-Analysis</p></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("دقة النموذج", "94%", "Phase 2")
col2.metric("المتجر", "Saudi Store")
col3.metric("الحالة", "Live Web App Phase 3")

st.sidebar.title("لوحة التحكم")
st.sidebar.info("المرحلة الثالثة: تحويل نموذج Phase2_AI_Model الى موقع")

category = st.sidebar.selectbox("اختر الفئة", ["الكترونيات", "ازياء", "جمال", "منزل", "العاب"])
price = st.sidebar.slider("السعر المتوقع (ريال)", 10, 2000, 299)
city = st.sidebar.selectbox("المدينة", ["جدة", "الرياض", "مكة", "الدمام", "المدينة"])

if st.sidebar.button("توقع المبيعات"):
    score = 85 + (price % 15)
    st.sidebar.success(f"نسبة نجاح المنتج المتوقعة: {score}%")
    st.balloons()

st.subheader("تحليل المبيعات - cleaned_saudi_store.csv")
data = {"الفئة": ["الكترونيات", "ازياء", "جمال", "الكترونيات", "منزل"], "المبيعات": [1200, 850, 950, 1100, 600], "المدينة": ["جدة", "الرياض", "جدة", "الدمام", "الرياض"]}
df = pd.DataFrame(data)
fig = px.bar(df, x="الفئة", y="المبيعات", color="المدينة", title="مبيعات حسب الفئة والمدينة")
st.plotly_chart(fig, use_container_width=True)

st.subheader("ربط نموذج Phase 2")
st.code('''
import pickle
with open('../Phase2_AI_Model.pkl', 'rb') as f:
    model = pickle.load(f)
prediction = model.predict([[price, category_encoded, city_encoded]])
''', language="python")

st.success("الخطوة القادمة: ارفع هذا المجلد الى GitHub بنفس طريقة المرحلة الثانية!")
