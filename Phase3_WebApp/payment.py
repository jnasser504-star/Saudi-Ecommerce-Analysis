import streamlit as st

st.subheader("💳 دفع آمن عبر Moyasar - بوابة الدفع السعودية")

st.markdown("""
- **Moyasar** هي بوابة دفع سعودية مرخصة من البنك المركزي
- تدعم: مدى، STC Pay، Apple Pay، 【entity-Visa¦canonical_name=Visa】
- رسوم: 2.8% + 1 ريال لكل عملية
""")

# هذا كود تجريبي - لما تسجل في moyasar.com يعطوك مفتاح حقيقي
if st.button("ادفع 49 ريال الآن عبر Moyasar"):
    st.success("✅ تم الدفع بنجاح! (تجريبي - في الحقيقي ستنتقل لصفحة Moyasar)")
    st.session_state['is_pro'] = True
    st.balloons()