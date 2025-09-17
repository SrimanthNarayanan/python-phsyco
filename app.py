import requests
import streamlit as st
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

BASE_URL = "https://app-main-eydcfpeyfmgtabec.centralindia-01.azurewebsites.net"

# Create FastAPI instance
api = FastAPI()

# Proxy endpoint: Power Automate will call this
@api.post("/analyze")
async def analyze(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "Total Sales In June")
    limit = body.get("limit", 1000)

    try:
        response = requests.post(f"{BASE_URL}/analyze", json={"prompt": prompt, "limit": limit})
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Streamlit UI for manual testing
def streamlit_ui():
    st.title("API Proxy for Power Automate")
    prompt = st.text_input("Prompt", "Total Sales In June")
    limit = st.number_input("Limit", 1000)
    if st.button("Send Request"):
        r = requests.post(f"{BASE_URL}/analyze", json={"prompt": prompt, "limit": limit})
        st.json(r.json())

if __name__ == "__main__":
    import threading
    def run_api():
        uvicorn.run(api, host="0.0.0.0", port=8000)
    threading.Thread(target=run_api, daemon=True).start()
    streamlit_ui()
