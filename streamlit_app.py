
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Assistant AI",
    page_icon="🤖"
)

st.title("🤖 Assistant AI")
st.caption("Your AI chatbot")

def get_api_key():
    key = os.getenv("GROQ_API_KEY", "").strip()

    if key:
        return key

    try:
        return st.secrets["GROQ_API_KEY"].strip()
    except (KeyError, FileNotFoundError):
        return ""

api_key = get_api_key()

if not api_key:
    st.error("Groq API key is missing. Configure it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Write your question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are Assistant AI. Give helpful, "
                                "accurate answers. Reply in the same "
                                "language as the user."
                            )
                        },
                        *st.session_state.messages
                    ],
                    temperature=0.5,
                    max_completion_tokens=1024
                )

                answer = response.choices[0].message.content
                if not answer:
                    answer = "No response received. Please try again."

                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )

        except Exception as e:
            st.error("The AI request failed.")
            st.caption(str(e))

if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()
