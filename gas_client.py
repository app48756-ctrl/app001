import time, hmac, hashlib, base64, json, requests, os

GAS_URL = os.environ.get("GAS_URL") or os.getenv("GAS_URL") or None
SHARED_SECRET = os.environ.get("SHARED_SECRET") or os.getenv("SHARED_SECRET") or None

def _signature(payload: str, timestamp: str) -> str:
    msg = f"{timestamp}\n{payload}".encode("utf-8")
    key = (SHARED_SECRET or "").encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

def gas_get(action: str, params: dict | None = None):
    url = f"{GAS_URL}?action={action}"
    return requests.get(url, params=params or {}, timeout=15).json()

def gas_post(action: str, payload: dict):
    ts = str(int(time.time()))
    body = {"action": action, "payload": payload, "X-Timestamp": ts}
    data = json.dumps(body, ensure_ascii=False)
    sig = _signature(data, ts)
    headers = {
        "Content-Type": "application/json",
        "X-Timestamp": ts,
        "X-Signature": sig,
    }
    resp = requests.post(GAS_URL, data=data.encode("utf-8"), headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()

def upload_file(name: str, content_bytes: bytes, mime: str | None = None):
    b64 = base64.b64encode(content_bytes).decode("ascii")
    return gas_post("upload_file", {"filename": name, "content_base64": b64, "mimeType": mime or "application/octet-stream"})
