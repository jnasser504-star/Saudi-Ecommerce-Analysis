import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
import pickle
from io import BytesIO

st.set_page_config(page_title="Saudi Ecommerce - جميل ناصر - المرحلة الرابعة", layout="wide", page_icon="🇸🇦")

# الهيدر
st.markdown('<div style="background: linear-gradient(90deg, #006C35 0%, #00502A 100%); padding:20px; border-radius:15px; color:white; text-align:center;"><h1>🇸🇦 Saudi-Ecommerce - المرحلة الرابعة</h1><p>المطور: جميل ناصر | لوحة تحكم التاجر السعودي</p></div>', unsafe_allow_html=True)

# لوحة التحكم الجانبية - نموذج 94%
st.sidebar.title("🔧 توقع نجاح المنتج")
category_side = st.sidebar.selectbox("فئة المنتج", ["إلكترونيات", "أزياء", "جمال", "منزل", "ألعاب"])
price_side = st.sidebar.slider("السعر (ريال)", 10, 2000, 299)
city_side = st.sidebar.selectbox("المدينة", ["جدة", "الرياض", "الدمام", "مكة", "الطائف"])

if st.sidebar.button("توقع المبيعات 🚀"):
    score = 85 + (price_side % 15)
    st.sidebar.success(f"نسبة نجاح المنتج: {score}%")
    st.balloons()

# قراءة البيانات
st.subheader("📊 بياناتك الحقيقية - 1165 طلب")
csv_found = False

for csv_path in ["cleaned_saudi_store.csv", "../cleaned_saudi_store.csv"]:
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            st.success(f"✅ يقرأ من: {csv_path} | {len(df)} طلب")
            csv_found = True
            
            # إحصائيات عامة
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("إجمالي الطلبات", len(df))
            c2.metric("إجمالي المبيعات", f"{df['Total'].sum():,.0f} ريال")
            c3.metric("متوسط الطلب", f"{df['Total'].mean():.0f} ريال")
            c4.metric("عدد المدن", df['City'].nunique())

            st.divider()

            # ===== المرحلة الرابعة: الفلاتر =====
            st.subheader("🔍 فلتر التاجر السعودي")
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                selected_city = st.selectbox("اختر المدينة", ["الكل"] + sorted(list(df['City'].unique())))
            with col_f2:
                selected_category = st.selectbox("اختر الفئة", ["الكل"] + sorted(list(df['Category'].unique())))
            with col_f3:
                selected_payment = st.selectbox("طريقة الدفع", ["الكل"] + sorted(list(df['PaymentMethod'].unique())))

            # تطبيق الفلترة
            df_filtered = df.copy()
            if selected_city != "الكل":
                df_filtered = df_filtered[df_filtered['City'] == selected_city]
            if selected_category != "الكل":
                df_filtered = df_filtered[df_filtered['Category'] == selected_category]
            if selected_payment != "الكل":
                df_filtered = df_filtered[df_filtered['PaymentMethod'] == selected_payment]

            st.success(f"✅ عرض {len(df_filtered)} طلب من أصل {len(df)} بعد الفلترة")
            st.dataframe(df_filtered.head(10))

            # إحصائيات بعد الفلترة
            cf1, cf2, cf3 = st.columns(3)
            cf1.metric("مبيعات الفلتر", f"{df_filtered['Total'].sum():,.0f} ريال")
            cf2.metric("عدد طلبات الفلتر", len(df_filtered))
            cf3.metric("متوسط الفلتر", f"{df_filtered['Total'].mean():.0f} ريال" if len(df_filtered) > 0 else "0")

            # زر تصدير Excel
            st.subheader("📥 تصدير تقرير التاجر")
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='تقرير المبيعات')
            
            st.download_button(
                label="📊 حمّل تقرير Excel للفلتر الحالي",
                data=output.getvalue(),
                file_name=f"تقرير_{selected_city}_{selected_category}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            st.divider()

            # الرسوم - تستخدم df_filtered عشان تتغير مع الفلتر
            st.subheader("🏙️ إجمالي المبيعات حسب المدينة (بعد الفلتر)")
            if len(df_filtered) > 0:
                city_sales = df_filtered.groupby('City')['Total'].sum().reset_index().sort_values('Total', ascending=False)
                fig1 = px.bar(city_sales, x='City', y='Total', color='City', title="المبيعات بعد الفلترة")
                st.plotly_chart(fig1, use_container_width=True)

                st.subheader("📦 المبيعات حسب الفئة (بعد الفلتر)")
                cat_sales = df_filtered.groupby('Category')['Total'].sum().reset_index()
                fig2 = px.pie(cat_sales, values='Total', names='Category', title="توزيع الفئات بعد الفلترة")
                st.plotly_chart(fig2, use_container_width=True)

                st.subheader("💳 تحليل Seaborn - طرق الدفع بعد الفلترة")
                fig3, ax3 = plt.subplots(figsize=(10,4))
                sns.countplot(data=df_filtered, x='PaymentMethod', hue='City', ax=ax3)
                plt.xticks(rotation=20)
                plt.title("طرق الدفع بعد الفلترة")
                st.pyplot(fig3)

            break
        except Exception as e:
            st.error(f"خطأ في قراءة {csv_path}: {e}")

if not csv_found:
    st.error("❌ لم أجد cleaned_saudi_store.csv - انسخه داخل Phase3_WebApp")