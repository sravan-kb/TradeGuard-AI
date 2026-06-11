import streamlit as st
from agent import analyze_entity
from entity_analyzer import check_entity

st.set_page_config(
    page_title="TradeGuard-AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ TradeGuard-AI")
st.subheader("AI-Powered Vendor Risk & Compliance Screening")

st.info("""
TradeGuard-AI screens vendors against public compliance datasets
and generates AI-powered risk assessments to support due diligence
and vendor onboarding reviews.
""")

entity = st.text_input(
    "Enter Company / Vendor Name"
)

if st.button("Analyze Vendor"):

    if not entity.strip():
        st.warning("Please enter a company or vendor name.")
        st.stop()

    with st.spinner("Screening vendor..."):
        screening_result = check_entity(entity)

    st.markdown("---")
    st.subheader("Vendor Screening Result")

    if screening_result.get("error"):
        st.warning(screening_result["error"])
        st.stop()

    # OFAC Result
    if screening_result["ofac_match"]:
        st.error(f"🔴 OFAC (USA Sanctions) — Match Found: {screening_result['matched_ofac']}")
    else:
        st.success("🟢 OFAC (USA Sanctions) — No Match Detected")

    # SEBI Result
    if screening_result["sebi_match"]:
        st.error(f"🔴 SEBI Debarred (India) — Match Found: {screening_result['matched_sebi']}")
    else:
        st.success("🟢 SEBI Debarred (India) — No Match Detected")

    with st.spinner("Generating AI assessment..."):
        result = analyze_entity(entity, screening_result)

    st.markdown("---")
    st.subheader("TradeGuard-AI Assessment")

    st.write(result)

    st.markdown("---")

    st.caption(
        "TradeGuard-AI presents findings for review. "
        "Final vendor decisions must be made by a qualified compliance officer."
    )