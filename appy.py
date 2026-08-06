import streamlit as st
from google import genai

st.set_page_config(page_title="Executive Report Cleaner", layout="wide")

st.title("📝 Executive Report Cleaner Agent")
st.caption("24/7 Cloud Service powered by Google Gemini AI")

SYSTEM_PROMPT = """You are an executive communications editor.
Rules:
1. Fix grammar, spelling, and sentence flow.
2. Remove profanity and slang.
3. NEVER make up or insert specific calendar dates (like February 22 or 24). If the text says "Yesterday", keep "Yesterday" or use "On the previous day".
4. DIRECT OUTPUT ONLY: Do NOT write conversational intros or explanations. Output ONLY the polished report text directly.
"""

def clean_report(raw_text: str) -> str:
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from Streamlit Secrets.")
        
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\nReport to clean:\n{raw_text}",
    )
    return response.text.strip()

# UI Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Employee Submission")
    default_draft = "Yesterday around 3:15pm the database server completely crashed because someone uploaded the wrong config script. We lost about 45 mins of downtime on line 2. Fixed it by 4pm and back running fine."
    raw_input = st.text_area("Paste draft here:", value=default_draft, height=280)
    process_btn = st.button("✨ Clean Report", type="primary", use_container_width=True)

with col2:
    st.subheader("Polished Executive Output")
    if process_btn and raw_input.strip():
        with st.spinner("Processing report..."):
            try:
                cleaned_result = clean_report(raw_input)
                st.code(cleaned_result, language=None)
                st.download_button(
                    label="📥 Download Cleaned Report (.txt)",
                    data=cleaned_result,
                    file_name="cleaned_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.success("Report successfully cleaned!")
            except Exception as err:
                st.error(f"Execution error: {err}")
    else:
        st.info("Paste a report draft on the left and click 'Clean Report'.")
