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
        matches = " | ".join(screening_result["matched_ofac"])
        st.error(f"🔴 OFAC (USA Sanctions) — {len(screening_result['matched_ofac'])} Match(es) Found: {matches}")
    else:
        st.success("🟢 OFAC (USA Sanctions) — No Match Detected")

    # SEBI Result
    if screening_result["sebi_match"]:
        matches = " | ".join(screening_result["matched_sebi"])
        st.warning(f"🟡 SEBI Debarred (India) — {len(screening_result['matched_sebi'])} Match(es) Found: {matches}")
    else:
        st.success("🟢 SEBI Debarred (India) — No Match Detected")

    with st.spinner("Generating AI assessment..."):
        result = analyze_entity(entity, screening_result)

    if result.strip().startswith("PERSON_DETECTED"):
        st.warning("Please enter a company or vendor name, not a person's name.")
        st.stop()

    st.markdown("---")
    st.subheader("TradeGuard-AI Assessment")

    sections = {
        "COMPANY OVERVIEW:": [],
        "SCREENING SUMMARY:": [],
        "VENDOR RISK ANALYSIS:": [],
        "COMPLIANCE EXPOSURE:": [],
        "RECOMMENDED DUE DILIGENCE ACTIONS:": [],
        "IMPORTANT NOTICE:": []
    }

    current_section = None
    risk_line = ""

    for line in result.split("\n"):
        line = line.strip()
        if not line:
            continue
        elif line.startswith("RISK LEVEL:"):
            risk_line = line.replace("RISK LEVEL:", "").strip()
        elif line in sections:
            current_section = line
        elif current_section:
            sections[current_section].append(line)

    # Risk Level
    if "High" in risk_line:
        st.error(f"🔴 Risk Level: {risk_line}")
    elif "Medium" in risk_line:
        st.warning(f"🟡 Risk Level: {risk_line}")
    else:
        st.success(f"🟢 Risk Level: {risk_line}")

    # Company Overview — full width
    if sections["COMPANY OVERVIEW:"]:
        st.markdown("**🏷️ Company Overview**")
        st.write(" ".join(sections["COMPANY OVERVIEW:"]))

    st.markdown("---")

    # Two column layout
    col1, col2 = st.columns(2)

    any_match = screening_result["ofac_match"] or screening_result["sebi_match"]

    with col1:
        st.markdown("**📋 Screening Summary**")
        st.info(" ".join(sections["SCREENING SUMMARY:"]))

        st.markdown("**⚠️ Compliance Exposure**")
        if any_match:
            st.error(" ".join(sections["COMPLIANCE EXPOSURE:"]))
        else:
            st.write(" ".join(sections["COMPLIANCE EXPOSURE:"]))

    with col2:
        st.markdown("**🏢 Vendor Risk Analysis**")
        if any_match:
            if "High" in risk_line:
                st.error(" ".join(sections["VENDOR RISK ANALYSIS:"]))
            else:
                st.write(" ".join(sections["VENDOR RISK ANALYSIS:"]))
        else:
            st.write(" ".join(sections["VENDOR RISK ANALYSIS:"]))

        st.markdown("**✅ Recommended Due Diligence Actions**")
        for item in sections["RECOMMENDED DUE DILIGENCE ACTIONS:"]:
            if any(item.startswith(f"{i}.") for i in range(1, 10)):
                st.markdown(item)

    st.markdown("---")

    if sections["IMPORTANT NOTICE:"]:
        st.caption(" ".join(sections["IMPORTANT NOTICE:"]))

    st.caption(
        "TradeGuard-AI presents findings for review. "
        "Final vendor decisions must be made by a qualified compliance officer."
    )