import os
import requests
import streamlit as st

BACKEND = st.secrets.get("BACKEND_URL", os.getenv("BACKEND_URL", ""))

st.title("Streamlit ↔ FastAPI (free)")
st.caption(f"Backend: {BACKEND or '(未設定)'}")

q = st.text_input("echo する文字列", "hello")
if st.button("送信"):
    if not BACKEND:
        st.error("BACKEND_URL が未設定です")
    else:
        r = requests.get(f"{BACKEND}/echo", params={"q": q}, timeout=15)
        st.json(r.json())
