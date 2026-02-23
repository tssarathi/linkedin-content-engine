import requests
import streamlit as st

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="LinkedIn Content Engine",
    page_icon="\U0001f916",
    layout="centered",
)

st.title("LinkedIn Content Engine")
st.caption("Enter a topic or paste a GitHub URL to generate a LinkedIn post.")

prompt = st.text_area(
    "Prompt",
    height=120,
    placeholder="e.g., Write a post about LangGraph https://github.com/langchain-ai/langgraph",
)

if st.button(
    "Generate", type="primary", use_container_width=True, disabled=not prompt.strip()
):
    with st.spinner("Generating post..."):
        try:
            response = requests.post(
                f"{API_BASE}/request",
                json={"prompt": prompt},
                timeout=300,
            )
            response.raise_for_status()
            post = response.json()["post"]
            st.session_state.generated_post = post
        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to backend. "
                "Run `uvicorn app.backend.api:app --reload` first."
            )
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                st.error("Gemini API rate limit exceeded. ")
            else:
                st.error(f"Generation failed: {e}")
        except Exception as e:
            st.error(f"Generation failed: {e}")

if st.session_state.get("generated_post"):
    st.divider()
    st.subheader("Generated Post")
    st.code(st.session_state.generated_post, language=None)
