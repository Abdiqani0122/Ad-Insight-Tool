import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY mangler. Sjekk .env-filen din.")
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Ad Insight Tool", layout="centered")

st.title("Ad Insight Tool")
st.write("Legg inn 3 tidligere annonser og deres CTR.")

st.subheader("Ad 1")
ad1_text = st.text_area(
    "Text",
    key="ad1_text",
    placeholder="Eksempel: Få flere leads på 30 dager – gratis analyse av annonseringen din."
)
ad1_ctr = st.number_input(
    "CTR (%)",
    min_value=0.0,
    step=0.1,
    key="ad1_ctr"
)

st.subheader("Ad 2")
ad2_text = st.text_area(
    "Text",
    key="ad2_text",
    placeholder="Eksempel: Vi hjelper bedrifter med digital markedsføring."
)
ad2_ctr = st.number_input(
    "CTR (%)",
    min_value=0.0,
    step=0.1,
    key="ad2_ctr"
)

st.subheader("Ad 3")
ad3_text = st.text_area(
    "Text",
    key="ad3_text",
    placeholder="Eksempel: Begrensede plasser – book en gratis vurdering i dag."
)
ad3_ctr = st.number_input(
    "CTR (%)",
    min_value=0.0,
    step=0.1,
    key="ad3_ctr"
)

analyze_button = st.button("Analyze Ads", key="analyze_ads_button")

if analyze_button:
    ads = [
        {"text": ad1_text, "ctr": ad1_ctr},
        {"text": ad2_text, "ctr": ad2_ctr},
        {"text": ad3_text, "ctr": ad3_ctr},
    ]

    ads = [ad for ad in ads if ad["text"].strip()]

    if len(ads) < 3:
        st.warning("Legg inn tekst for alle 3 annonser.")
    else:
        st.success("Input er klar for analyse.")

        sorted_ads = sorted(ads, key=lambda x: x["ctr"], reverse=True)
        top_ads = sorted_ads[:2]
        low_ads = sorted_ads[-1:]

        st.subheader("🏆 Top performing ads")
        st.json(top_ads)

        st.subheader("⚠️ Low performing ads")
        st.json(low_ads)

        prompt = f"""
You are a senior marketing strategist at a performance marketing agency.

Your job is to analyze past ad variations and extract clear, actionable learnings for future campaigns.

Important constraints:
- Do NOT generate new ads
- Do NOT rewrite ads
- Do NOT be generic
- Focus only on analysis and decision support
- Base all insights ONLY on the provided data

Your task:
Compare high-performing ads vs low-performing ads and identify patterns that explain performance differences.

Be specific. Every insight must be grounded in actual examples from the ads.

---

DATA:

Top-performing ads:
{top_ads}

Low-performing ads:
{low_ads}

All ads:
{ads}

---

OUTPUT FORMAT:

### What worked (patterns in high-performing ads)
- Identify 3–5 specific patterns
- Explain WHY they likely improved performance
- Reference actual phrases or structures from the ads

### What didn’t work (patterns in low-performing ads)
- Identify 2–4 weaknesses
- Explain WHY these reduce engagement
- Be concrete (e.g., “generic phrasing”, “no clear outcome”)

### Extracted hooks / messaging styles
- List the core persuasive angles used
- Examples: urgency, specificity, social proof, outcome-driven, etc.

### Recommendations (3–5 actionable rules)
- Write as clear instructions a marketing team can follow
- Focus on WHAT to do and WHY
- Avoid vague advice

### Playbook summary (max 3 sentences)
- Summarize the key strategic takeaway
- Make it reusable for future campaigns

---

Quality bar:
- No generic statements
- No fluff
- No repetition
- Prioritize clarity, specificity, and usefulness
"""

        with st.spinner("Analyzing patterns and learnings..."):
            try:
                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )
                result = response.output_text
            except Exception as e:
                st.error(f"API-feil: {e}")
                st.stop()

        st.subheader("AI Insights")
        st.markdown(result)