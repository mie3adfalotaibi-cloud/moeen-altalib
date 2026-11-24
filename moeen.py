import streamlit as st
import re

# ---------- الإعدادات والتصميم ----------
st.set_page_config(page_title="مُعين الطالب", page_icon="📘", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
html, body, [class*="css"], .stApp, p, label, span, div, li, input, textarea {
    font-family: 'Tajawal', sans-serif !important;}
.stApp {direction: rtl; text-align: right; background: #5B7C99 !important;}
p, label, span, div, li, h1, h2, h3 {color: #FFFFFF !important;}

.header {background: #4A6880; border-radius: 16px; padding: 28px; margin-bottom: 16px;
         border-bottom: 4px solid #F2D388; text-align: center;}
.brand {color: #F2D388 !important; font-size: 40px; font-weight: 700;}
.sub {color: #E8EEF4 !important; font-size: 15px; margin-top: 4px;}

.card {background: #4A6880; border: 1px solid #6E8CA6; border-right: 5px solid #F2D388;
       border-radius: 12px; padding: 14px 18px; margin-bottom: 10px;}
.num {background: #F2D388; color: #2E4458 !important; border-radius: 50%; padding: 1px 9px;
      font-weight: 700; margin-left: 8px;}
.stButton button {background: #F2D388 !important; border: none; border-radius: 10px; padding: 8px 28px;}
.stButton button p {color: #2E4458 !important; font-weight: 700;}
.stButton button:hover {background: #F5DFA0 !important;}
.stTextArea textarea {background: #FFFFFF !important; color: #2B2B2B !important; border-radius: 10px;}
[data-testid="stMetric"] {background: #4A6880; border: 1px solid #6E8CA6; border-radius: 12px; padding: 10px;}
[data-testid="stMetricValue"] div {color: #F2D388 !important;}
.stDownloadButton button {background: #F2D388 !important; border: none; border-radius: 10px;}
.stDownloadButton button p {color: #2E4458 !important; font-weight: 700;}
.foot {text-align: center; margin-top: 40px; padding-top: 16px; border-top: 1px solid #6E8CA6;
       color: #D8E2EC !important; font-size: 13px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
  <div class="brand">مُعين الطالب</div>
  <div class="sub">خدمات طلابية للجامعات والمدارس</div>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📘 محوّل الملخصات")
st.write("الصق نص المحاضرة أو الدرس، واحصل على ملخص بأهم النقاط.")

text = st.text_area("نص الدرس", height=240, placeholder="الصق النص هنا...")

n = st.slider("عدد نقاط الملخص", 3, 10, 5)

def split_sentences(t):
    parts = re.split(r'[.!؟?\n]+', t)
    return [p.strip() for p in parts if len(p.strip()) > 20]

def summarize(t, count):
    sentences = split_sentences(t)
    if not sentences:
        return []
    words = re.findall(r'[\u0600-\u06FFa-zA-Z]+', t.lower())
    freq = {}
    for w in words:
        if len(w) > 2:
            freq[w] = freq.get(w, 0) + 1
    scored = []
    for i, s in enumerate(sentences):
        sw = re.findall(r'[\u0600-\u06FFa-zA-Z]+', s.lower())
        score = sum(freq.get(w, 0) for w in sw) / (len(sw) + 1)
        scored.append((score, i, s))
    top = sorted(scored, reverse=True)[:count]
    top = sorted(top, key=lambda x: x[1])
    return [s for _, _, s in top]

if st.button("لخّص"):
    if not text.strip():
        st.warning("الصق النص أولاً.")
    else:
        points = summarize(text, n)
        if not points:
            st.warning("النص قصير جداً، أضف نصاً أطول.")
        else:
            st.markdown("### أهم النقاط")
            for i, p in enumerate(points, 1):
                dot = "" if p.endswith(('.', '؟', '!')) else "."
                st.markdown(f"<div class='card'><span class='num'>{i}</span>{p}{dot}</div>",
                            unsafe_allow_html=True)

            words_before = len(text.split())
            words_after = len(" ".join(points).split())
            c1, c2, c3 = st.columns(3)
            c1.metric("كلمات النص", words_before)
            c2.metric("كلمات الملخص", words_after)
            saved = round((1 - words_after / words_before) * 100) if words_before else 0
            c3.metric("اختصار", f"{saved}%")

            out = "ملخص - مُعين الطالب\n\n"
            for i, p in enumerate(points, 1):
                dot = "" if p.endswith((".", "؟", "!")) else "."
                out += f"{i}. {p}{dot}\n"
            st.download_button("تحميل الملخص", out, file_name="summary.txt")

st.markdown("""
<div class="foot">
  مُعين الطالب · خدمات طلابية للجامعات والمدارس
</div>
""", unsafe_allow_html=True)