"""Task 1: Language Translation Tool (Streamlit + Google Translate via deep-translator)."""
import io
import streamlit as st
import streamlit.components.v1 as components
from deep_translator import GoogleTranslator
from gtts import gTTS

st.set_page_config(page_title="Language Translator", page_icon="🌐")
st.title("🌐 Language Translation Tool")

LANGS = {"Auto Detect": "auto", **{n.title(): c for n, c in GoogleTranslator().get_supported_languages(as_dict=True).items()}}
TARGETS = {k: v for k, v in LANGS.items() if v != "auto"}

c1, c2 = st.columns(2)
src = c1.selectbox("From", list(LANGS), index=0)
tgt = c2.selectbox("To", list(TARGETS), index=list(TARGETS).index("Spanish"))
text = st.text_area("Enter text", height=150, max_chars=4500)

if st.button("Translate", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        try:
            st.session_state["result"] = GoogleTranslator(source=LANGS[src], target=TARGETS[tgt]).translate(text)
            st.session_state["tgt_code"] = TARGETS[tgt]
        except Exception as e:
            st.error(f"Translation failed: {e}")

if "result" in st.session_state:
    result = st.session_state["result"]
    st.subheader("Translation")
    st.success(result)
    # Copy button
    safe = result.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    components.html(
        f"""<button onclick="navigator.clipboard.writeText(`{safe}`);this.innerText='Copied ✓'"
        style="padding:8px 16px;border-radius:6px;border:1px solid #888;cursor:pointer">📋 Copy</button>""",
        height=50,
    )
    # Text-to-speech
    if st.button("🔊 Speak"):
        try:
            buf = io.BytesIO()
            gTTS(result, lang=st.session_state["tgt_code"]).write_to_fp(buf)
            st.audio(buf.getvalue(), format="audio/mp3")
        except Exception as e:
            st.error(f"Speech not available for this language: {e}")
