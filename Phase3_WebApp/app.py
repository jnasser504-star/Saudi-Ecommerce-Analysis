import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import BytesIO

st.set_page_config(page_title="Saudi Ecommerce - جميل ناصر", layout="wide", page_icon="🇸🇦")

st.markdown('<div style="background: linear-gradient(90deg, #006C35 0%, #00502A 100%); padding:20px; border-radius:15px; color:white; text-align:center;"><h1>🇸🇦 Saudi-Ecommerce - المرحلة الخامسة</h1><p>المطور: جميل ناصر | لوحة تحكم + تصدير</p></div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔧 توقع نجاح المنتج")
cat_side = st.sidebar.selectbox("فئة المنتج", ["إلكترونيات", "أزياء", "جمال", "منزل"])
price_side = st.sidebar.slider("السعر (ريال)", 10, 2000, 299)
city_side = st.sidebar.selectbox("المدينة", ["جدة", "الرياض", "الدمام"])
if st.sidebar.button("توقع 🚀"):
    st.sidebar.success(f"نسبة النجاح: {85 + price_side % 15}%")
    st.balloons()

# قراءة البيانات
st.subheader("📊 بياناتك الحقيقية")
df = None
for csv_path in ["cleaned_saudi_store.csv", "../cleaned_saudi_store.csv"]:
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.success(f"✅ يقرأ من: {csv_path} | {len(df)} طلب")
        break

if df is None:
    st.error("❌ لم أجد cleaned_saudi_store.csv")
    st.stop()

# إحصائيات
c1, c2, c3, c4 = st.columns(4)
c1.metric("إجمالي الطلبات", len(df))
c2.metric("إجمالي المبيعات", f"{df['Total'].sum():,.0f} ريال")
c3.metric("متوسط الطلب", f"{df['Total'].mean():.0f} ريال")
c4.metric("عدد المدن", df['City'].nunique())

st.divider()

# فلتر التاجر
st.subheader("🔍 فلتر التاجر السعودي")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    selected_city = st.selectbox("المدينة", ["الكل"] + sorted(list(df['City'].unique())))
with col_f2:
    selected_category = st.selectbox("الفئة", ["الكل"] + sorted(list(df['Category'].unique())))
with col_f3:
    selected_payment = st.selectbox("الدفع", ["الكل"] + sorted(list(df['PaymentMethod'].unique())))

df_filtered = df.copy()
if selected_city != "الكل":
    df_filtered = df_filtered[df_filtered['City'] == selected_city]
if selected_category != "الكل":
    df_filtered = df_filtered[df_filtered['Category'] == selected_category]
if selected_payment != "الكل":
    df_filtered = df_filtered[df_filtered['PaymentMethod'] == selected_payment]

st.success(f"✅ عرض {len(df_filtered)} طلب من أصل {len(df)}")

# زر Excel - النسخة المحمية للمرحلة الخامسة
st.subheader("📥 تصدير تقرير التاجر")

output = BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_filtered.to_excel(writer, index=False, sheet_name='تقرير المبيعات')

if 'is_pro' in st.session_state and st.session_state['is_pro']:
    st.success("✅ مشترك - التحميل متاح")
    st.download_button(
        label="📊 حمّل Excel",
        data=output.getvalue(),
        file_name=f"تقرير_{selected_city}_{selected_category}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("🔒 Excel للمشتركين فقط - 49 ريال")
    if st.button("🔓 ادفع 49 ريال وافتح التحميل"):
        st.session_state['is_pro'] = True
        st.rerun()

st.divider()

# الرسوم
st.subheader("🏙️ المبيعات حسب المدينة")
if len(df_filtered) > 0:
    city_sales = df_filtered.groupby('City')['Total'].sum().reset_index().sort_values('Total', ascending=False)
    fig1 = px.bar(city_sales, x='City', y='Total', color='City')
    st.plotly_chart(fig1, use_container_width=True)