
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# -------------------- Configuration --------------------

st.set_page_config(
    page_title="Assistant AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
)

SYSTEM_PROMPT = """
You are Assistant AI, a helpful, intelligent and friendly AI assistant.

LANGUAGE RULES:
1. Understand English, Bengali (Bangla), and Banglish
   (Bengali written using English letters).
2. Detect the language and writing style of the user's message.
3. Reply in the same language and style the user uses.
4. If the user mixes Bangla and English, understand the
   complete meaning and respond naturally.
5. Understand informal spelling, common typos, and
   conversational Banglish when possible.
6. Do not translate the user's message unless requested.
7. Never claim that you understand something if you do not.

ANSWER RULES:
- Be accurate, clear, practical and friendly.
- Explain technical topics step by step when appropriate.
- Use examples and code blocks when useful.
- For Python code, prioritize complete, runnable solutions.
- Admit uncertainty instead of inventing facts.
- Remember the conversation context provided to you.
- Do not unnecessarily repeat the user's question.
- Use readable formatting and concise explanations.
"""

# -------------------- Custom Styling --------------------

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --accent: #7966FF;
        --accent2: #A78BFA;
    }

    .stApp {
        font-family: 'Inter', sans-serif;
        background:
            radial-gradient(
                ellipse at 12% 0%,
                rgba(121,102,255,0.11),
                transparent 38%
            );
    }

    .block-container {
        max-width: 1050px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.18);
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 13px;
        margin-bottom: 22px;
    }

    .brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 49px;
        height: 49px;
        border-radius: 16px;
        background: linear-gradient(135deg, #7966FF, #B47AFF);
        color: white;
        font-size: 25px;
        box-shadow: 0 7px 24px rgba(121,102,255,0.25);
    }

    .brand-title {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.7px;
    }

    .muted {
        color: #8B8D9A;
        font-size: 12px;
    }

    .hero {
        text-align: center;
        padding: 48px 10px 22px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 30px;
        border: 1px solid rgba(121,102,255,0.3);
        background: rgba(121,102,255,0.09);
        color: #A99BFF;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 20px;
    }

    .hero h1 {
        font-size: clamp(32px, 5vw, 49px);
        line-height: 1.15;
        letter-spacing: -1.8px;
        font-weight: 800;
        margin: 0 0 14px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #8877FF, #D09AFF);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .hero p {
        color: #8B8D9A;
        font-size: 15px;
        line-height: 1.8;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid rgba(128,128,128,0.13);
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 12px;
    }

    [data-testid="stChatInput"] {
        border-radius: 18px;
    }

    .stButton > button {
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: #8877FF;
        color: #A99BFF;
    }

    .footer-note {
        text-align: center;
        color: #898B98;
        font-size: 11px;
        padding: 16px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- Session State --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = DEFAULT_MODEL

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.5

# -------------------- Sidebar --------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-title">Assistant AI</div>
                <div class="muted">Your AI companion</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if st.button(
        "＋  New conversation",
        use_container_width=True,
        type="primary",
    ):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### ⚙️ Settings")

    model_options = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
    ]

    selected_model = st.selectbox(
        "AI Model",
        options=model_options,
        index=(
            model_options.index(st.session_state.model)
            if st.session_state.model in model_options
            else 0
        ),
        help="The larger model may have different usage limits.",
    )

    st.session_state.model = selected_model

    st.session_state.temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.temperature),
        step=0.1,
    )

    st.markdown("---")

    st.markdown("### 🌐 Languages")
    st.caption("🇧🇩 বাংলা")
    st.caption("🇬🇧 English")
    st.caption("💬 Banglish")

    st.markdown("---")
    st.markdown("### 💡 Try asking")

    examples = [
        "Explain Python in Bangla",
        "Amake AI shikhte help koro",
        "What is machine learning?",
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example
            st.rerun()

    st.markdown("---")
    st.caption("Powered by Groq API")
    st.caption("Built with Python + Streamlit")

# -------------------- Main Header --------------------

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">✦</div>
        <div>
            <div class="brand-title">Assistant AI</div>
            <div class="muted">
                Intelligent conversations, your way
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- Welcome Screen --------------------

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">
                ✨ YOUR PERSONAL AI ASSISTANT
            </div>
            <h1>
                Ask anything.<br>
                <span class="gradient-text">Explore everything.</span>
            </h1>
            <p>
                তোমার প্রশ্ন করো বাংলায়, English-এ অথবা Banglish-এ।<br>
                Let's learn, create and solve problems together.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 💻 Coding")
        st.caption("Python, debugging & software development")

    with col2:
        st.markdown("#### 🧠 Learn")
        st.caption("AI, ML, Deep Learning & new concepts")

    with col3:
        st.markdown("#### ✍️ Create")
        st.caption("Ideas, writing & problem solving")

# -------------------- Chat History --------------------

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "✨"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# -------------------- Groq API --------------------

def get_groq_client():
    """Create a Groq client without exposing the API key."""

    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "").strip()
        except Exception:
            api_key = ""

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY পাওয়া যায়নি। "
            "Project-এর .env file-এ API key যোগ করো।"
        )

    return Groq(api_key=api_key)


def generate_reply():
    """Generate an answer using the recent conversation context."""

    client = get_groq_client()

    # Keep a bounded conversation history.
    recent_messages = st.session_state.messages[-20:]

    response = client.chat.completions.create(
        model=st.session_state.model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *recent_messages,
        ],
        temperature=st.session_state.temperature,
        max_completion_tokens=2048,
    )

    answer = response.choices[0].message.content

    if not answer or not answer.strip():
        return "দুঃখিত, এবার কোনো উত্তর পাওয়া যায়নি। আবার চেষ্টা করো।"

    return answer.strip()


# -------------------- Input & Response --------------------

pending_prompt = st.session_state.pop("pending_prompt", None)

prompt = st.chat_input(
    "Message Assistant AI... / এখানে প্রশ্ন লেখো"
)

if pending_prompt:
    prompt = pending_prompt

if prompt and prompt.strip():
    prompt = prompt.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="✨"):
        try:
            with st.spinner("Assistant AI is thinking..."):
                answer = generate_reply()

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except ValueError as exc:
            st.error(str(exc))

        except Exception as exc:
            # Keep technical details in the local server logs.
            print(f"Groq API error: {type(exc).__name__}: {exc}")

            st.error(
                "উত্তর তৈরি করা যায়নি। Internet connection, "
                "API key, model availability ও Groq usage limits "
                "পরীক্ষা করে আবার চেষ্টা করো।"
            )

    st.rerun()

st.markdown(
    """
    <div class="footer-note">
        AI can make mistakes. Verify important information.
        <br>Assistant AI · Python × Groq
    </div>
    """,
    unsafe_allow_html=True,
)
