import os, uuid, datetime
import streamlit as st
from gas_client import gas_get, gas_post, upload_file

st.set_page_config(page_title="Free Stack: Streamlit × GAS × Google", page_icon="🧩", layout="centered")

# secrets を環境変数に反映（Community Cloud では自動で入ります）
os.environ.setdefault("GAS_URL", st.secrets["GAS_URL"])
os.environ.setdefault("SHARED_SECRET", st.secrets["SHARED_SECRET"])

st.title("🧩 無料スタック：Streamlit × GAS × Google")

with st.expander("接続テスト", expanded=False):
    try:
        health = gas_get("health")
        st.success(f"OK: {health}")
    except Exception as e:
        st.error(f"GAS接続エラー: {e}")

st.subheader("✅ TODO（Sheets）")
with st.form("todo_add", clear_on_submit=True):
    title = st.text_input("タイトル", placeholder="やること…")
    submitted = st.form_submit_button("追加")
    if submitted and title.strip():
        payload = {
            "id": str(uuid.uuid4()),
            "title": title.strip(),
            "done": False,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        }
        res = gas_post("add_todo", payload)
        if res.get("ok"):
            st.success("追加しました")
        else:
            st.error(f"失敗: {res}")

if st.button("最新のTODOを読む"):
    data = gas_get("list_todos")
    st.write(data.get("items", []))

st.subheader("📦 ファイルアップロード（Drive）")
file = st.file_uploader("ファイルを選択", type=None)
if file is not None:
    res = upload_file(file.name, file.read(), file.type)
    if res.get("ok"):
        st.success(f"アップロード完了: {res.get('name')} (id={res.get('fileId')})")
    else:
        st.error(f"失敗: {res}")
