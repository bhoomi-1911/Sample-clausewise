import streamlit as st
import time

st.set_page_config(page_title="ClauseWise", page_icon="⚖️", layout="wide")

# ---------- Mock Data ----------
analysis_results = {
    "docType": "Non-Disclosure Agreement (NDA)",
    "riskScore": 7.2,
    "complexityBefore": 22,
    "complexityAfter": 8,
    "complexityReduction": 73,
    "entities": {
        "parties": ["Acme Corporation", "John Smith"],
        "dates": ["January 1, 2024", "December 31, 2026"],
        "monetary": ["$50,000", "$10,000 per violation"],
        "terms": ["Confidential Information", "Trade Secrets"]
    },
    "clauses": [
        {
            "id": 1,
            "title": "Definition of Confidential Information",
            "original": 'The term "Confidential Information" shall mean all information, technical data, trade secrets, know-how, research, product plans...',
            "simplified": 'Confidential Information means private business information shared by the company.',
            "eli5": "It's like when your friend tells you a secret — this is all the secret stuff the company will share with you.",
            "professional": "Confidential Information includes all proprietary data like intellectual property and business strategies.",
            "risk": "high",
            "riskReason": "Very broad definition - covers almost any information you learn"
        },
        {
            "id": 2,
            "title": "Non-Disclosure Obligations",
            "original": "The Receiving Party agrees to hold and maintain the Confidential Information in strict confidence...",
            "simplified": "You must keep all confidential info secret and share only if needed for work.",
            "eli5": "You can't tell anyone the secrets, except teammates who need to know.",
            "professional": "Recipient must maintain confidentiality and limit disclosure to authorized personnel.",
            "risk": "medium",
            "riskReason": "Standard confidentiality clause"
        },
        {
            "id": 3,
            "title": "Term and Duration",
            "original": "This Agreement shall commence on the Effective Date and continue for 5 years...",
            "simplified": "This agreement lasts for 5 years from the start date.",
            "eli5": "You have to keep the secrets for 5 whole years — a long time!",
            "professional": "The confidentiality obligation extends for five years from the effective date.",
            "risk": "high",
            "riskReason": "5 years is longer than industry standard"
        },
        {
            "id": 4,
            "title": "Remedies",
            "original": "The Receiving Party acknowledges that disclosure would cause irreparable harm...",
            "simplified": "If you break this, the company can take you to court immediately.",
            "eli5": "If you tell the secrets, the company can make you stop right away.",
            "professional": "Breach allows the disclosing party to seek injunctive relief beyond damages.",
            "risk": "medium",
            "riskReason": "Standard legal remedy clause"
        }
    ],
    "redFlags": [
        "Confidential information definition is very broad",
        "Non-disclosure period exceeds industry standard",
        "No return/destruction of materials clause specified",
        "Unlimited liability for breaches"
    ],
    "greenFlags": [
        "Clear termination terms",
        "Allows disclosure to employees with need-to-know",
        "Standard governing law provisions"
    ]
}

# ---------- App Header ----------
st.markdown(
    """
    <h1 style="text-align:center; color:#1e3a8a;">⚖️ ClauseWise</h1>
    <p style="text-align:center; color:gray;">Legal Clarity for Everyone</p>
    """, unsafe_allow_html=True
)

st.divider()

# ---------- Upload or Demo ----------
if "show_results" not in st.session_state:
    st.session_state.show_results = False
    st.session_state.file_name = None

if not st.session_state.show_results:
    st.header("Understand Your Legal Documents in Seconds")
    st.write("Upload any contract to get AI-powered risk and clause insights.")

    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt"])
    col1, col2 = st.columns(2)

    with col1:
        if uploaded_file:
            with st.spinner("Analyzing your document..."):
                time.sleep(3)
                st.session_state.show_results = True
                st.session_state.file_name = uploaded_file.name
                st.rerun()

    with col2:
        if st.button("📄 Analyze Sample NDA"):
            with st.spinner("Analyzing sample NDA..."):
                time.sleep(3)
                st.session_state.show_results = True
                st.session_state.file_name = "Sample_NDA.pdf"
                st.rerun()

# ---------- Results Page ----------
else:
    if st.button("← Upload New Document"):
        st.session_state.show_results = False
        st.rerun()

    st.subheader(f"📄 {analysis_results['docType']}")
    st.caption(f"Document: {st.session_state.file_name}")

    # Dashboard
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Overall Risk Score", analysis_results["riskScore"], "High")
    with c2:
        st.metric("Complexity Reduced", f"{analysis_results['complexityReduction']}%",
                  f"{analysis_results['complexityBefore']} → {analysis_results['complexityAfter']}")
    with c3:
        st.metric("Clauses Analyzed", len(analysis_results["clauses"]))

    tab1, tab2, tab3 = st.tabs(["Clause Analysis", "Key Entities", "Ask Questions"])

    # ---------- Tab 1: Clause Analysis ----------
    with tab1:
        mode = st.radio(
            "Explanation Mode",
            ["ELI5", "Simplified", "Professional"],
            horizontal=True
        )

        st.markdown("### ⚠️ Red Flags Found")
        for flag in analysis_results["redFlags"]:
            st.error(flag)

        st.markdown("### ✅ Positive Aspects")
        for flag in analysis_results["greenFlags"]:
            st.success(flag)

        st.markdown("### 📜 Clauses")
        for clause in analysis_results["clauses"]:
            risk_color = {
                "high": "🔴 High",
                "medium": "🟡 Medium",
                "low": "🟢 Low"
            }.get(clause["risk"], "⚪ Unknown")

            st.markdown(f"#### {clause['title']} ({risk_color})")
            st.caption(f"⚠️ {clause['riskReason']}")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original:**")
                st.write(clause["original"])
            with col2:
                st.markdown(f"**{mode} Explanation:**")
                text = clause[mode.lower()]
                st.write(text)
                if st.button(f"🔊 Read '{clause['title']}' aloud", key=f"tts_{clause['id']}"):
                    st.toast(f"Reading aloud: {text}")

    # ---------- Tab 2: Entities ----------
    with tab2:
        st.subheader("👥 Parties Involved")
        st.write(", ".join(analysis_results["entities"]["parties"]))

        st.subheader("📅 Important Dates")
        st.write(", ".join(analysis_results["entities"]["dates"]))

        st.subheader("💰 Monetary Values")
        st.write(", ".join(analysis_results["entities"]["monetary"]))

        st.subheader("📋 Key Legal Terms")
        st.write(", ".join(analysis_results["entities"]["terms"]))

    # ---------- Tab 3: Chat ----------
    with tab3:
        st.write("💬 Ask questions about your contract:")
        if "chat" not in st.session_state:
            st.session_state.chat = []

        for msg in st.session_state.chat:
            if msg["type"] == "user":
                st.chat_message("user").write(msg["text"])
            else:
                st.chat_message("assistant").write(msg["text"])

        user_input = st.chat_input("Ask a question...")

        if user_input:
            st.session_state.chat.append({"type": "user", "text": user_input})
            lower = user_input.lower()

            responses = {
                "can i work for competitors": "There’s no non-compete clause. You can work for competitors, just don’t share confidential info.",
                "how long": "Confidentiality lasts 5 years, longer than the 2–3 year norm.",
                "what happens if i break": "The company can take you to court (injunction) and seek damages."
            }

            response = responses.get(lower, "I can help explain specific clauses. Try asking about duration, risks, or breaking terms.")
            st.session_state.chat.append({"type": "ai", "text": response})
            st.rerun()

# ---------- Footer ----------
st.divider()
st.caption("ClauseWise - Legal Clarity for Everyone | ⚠️ Demo Only. Not legal advice.")
