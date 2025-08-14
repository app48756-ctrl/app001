# app.py
import os
import requests
import streamlit as st

st.set_page_config(page_title="Streamlit → GAS → Sheets", layout="centered")

DEFAULT_URL = os.environ.get("GAS_URL", "")  # 環境変数でも指定可
gas_url = st.text_input("GAS Web App URL (/exec)", value=DEFAULT_URL, placeholder="https://script.google.com/macros/s/.../exec")

colA, colB, colC = st.columns(3)

with colA:
    if st.button("Health (GET)"):
        if not gas_url:
            st.error("URL を入力してください")
        else:
            try:
                r = requests.get(gas_url, params={"action": "health"}, timeout=10)
                st.write("status:", r.status_code)
                st.json(r.json())
            except Exception as e:
                st.error(str(e))

with colB:
    read_range = st.text_input("Read range (A1)", value="A1")
    if st.button("Read (GET)"):
        if not gas_url:
            st.error("URL を入力してください")
        else:
            try:
                r = requests.get(gas_url, params={"action": "read", "range": read_range}, timeout=10)
                st.write("status:", r.status_code)
                st.json(r.json())
            except Exception as e:
                st.error(str(e))

with colC:
    write_range = st.text_input("Write range (A1)", value="A1")
    write_value = st.text_input("Write value", value="hello")
    if st.button("Write (POST)"):
        if not gas_url:
            st.error("URL を入力してください")
        else:
            try:
                payload = {"action": "write", "value": write_value, "range": write_range}
                r = requests.post(gas_url, json=payload, timeout=10)
                st.write("status:", r.status_code)
                st.json(r.json())
            except Exception as e:
                st.error(str(e))
