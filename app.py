from core.pipeline import full_pipeline
from leads.database import database_connection, table_creation
from leads.notifier import notifier
import streamlit as st
import streamlit.components.v1 as components
from config.logger import logger
st.set_page_config(
    page_title="AI Dental Clinic Assistant Demo",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# ──────────────────────────────────────────────────────────────────────────
# CSS — exact visual match to the original HTML design
# ──────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
    :root {
        --primary: #01324a;
        --primary-soft: rgba(1, 50, 74, 0.08);
        --primary-border: rgba(1, 50, 74, 0.18);
        --ink: #05080a;
        --muted: rgba(5, 8, 10, 0.56);
        --line: rgba(1, 50, 74, 0.14);
    }
    html, body, [class*="css"] {
    font-family: 'Inter', "Segoe UI", Arial, sans-serif;
    }
    .stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(1, 50, 74, 0.55), transparent 50%),
        radial-gradient(circle at 90% 30%, rgba(1, 50, 74, 0.4), transparent 45%),
        radial-gradient(circle at 30% 95%, rgba(1, 50, 74, 0.35), transparent 45%),
        linear-gradient(180deg, #05080a 0%, #071a24 45%, #05080a 100%);
    }
    /* max-width / padding-bottom kept here; padding-top is set once
       below (2rem) instead of being declared twice like before */
    .block-container {
    max-width: 1500px;
    padding-top: 4.5rem;
    padding-bottom: 90px;
    }
    /* Eyebrow */
    .eyebrow { display: flex; justify-content: center; margin-bottom: 10px; }
    .eyebrow span {
        display: inline-flex; align-items: center; gap: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11.5px; letter-spacing: 0.14em; text-transform: uppercase;
        color: rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.16);
        padding: 7px 14px; border-radius: 999px;
    }
    .pulse-dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #4ADE80; display: inline-block;
        box-shadow: 0 0 0 0 rgba(74,222,128,0.6);
        animation: livePulse 2s infinite;
    }
    @keyframes livePulse {
        0% { box-shadow: 0 0 0 0 rgba(74,222,128,0.55); }
        70% { box-shadow: 0 0 0 7px rgba(74,222,128,0); }
        100% { box-shadow: 0 0 0 0 rgba(74,222,128,0); }
    }
    /* Hero Section */
        h1.hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600; font-size: 42px; line-height: 1.18;
        letter-spacing: -0.01em; text-align: center; color: #fff;
        margin: 10px 0 24px;
    }
    .lede {
        text-align: center; font-size: 16.5px; line-height: 1.65;
        color: rgba(255,255,255,0.68); max-width: 600px; margin: 0 auto 10px;
    }
    .lede.secondary { 
        color: rgba(255,255,255,0.52); max-width: 640px; 
        text-align: center; font-size: 16.5px; line-height: 1.65;
        
    }
    .features-heading {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600;
        font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase;
        color: rgba(255,255,255,0.45); text-align: center; margin: 56px 0 26px;
    }
    .features-heading::before, .features-heading::after {
        content: ''; display: inline-block; width: 28px; height: 1px;
        background: rgba(255,255,255,0.2); vertical-align: middle; margin: 0 14px;
    }
    /* Feature Cards */
    .feature-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px; padding: 24px 20px; height: 190px;
    display: flex; flex-direction: column;
    transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
    min-height: 190px;
    height: auto;
    }
    .feature-card:hover {
        transform: translateY(-3px);
        border-color: rgba(1, 50, 74, 0.6);
        background: rgba(1, 50, 74, 0.18);
    }
    .feature-card .icon {
        width: 40px; height: 40px; border-radius: 10px;
        background: var(--primary); border: 1px solid rgba(255,255,255,0.15);
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 14px; color: #fff; flex-shrink: 0;
    }
    .feature-card h3 {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600;
        font-size: 15.5px; color: #fff; line-height: 1.3;
        min-height: 40px; margin-bottom: 8px; flex-shrink: 0;
    }
    .feature-card p {
        font-size: 13.5px; line-height: 1.55; color: rgba(255,255,255,0.55); margin: 0;
    }
    /* Demo CTA */
    .demo-cta { text-align: center; margin: 70px 0 10px; }
    .demo-cta h2 {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600;
        font-size: 26px; color: #fff; margin-bottom: 12px;
    }
    .demo-cta p {
        font-size: 15px; line-height: 1.6; color: rgba(255,255,255,0.6);
        max-width: 520px; margin: 0 auto;
    }
    .demo-arrow {
        display: flex; justify-content: center; margin-top: 20px;
        color: rgba(255,255,255,0.35); animation: bounce 2.2s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(6px); }
    }
    .message {
    max-width: 75%;
    padding: 12px 16px;
    margin: 10px 0;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.6;
    color: white;
    word-wrap: break-word;
    }
    /* User bubble */
    .message.user {
        margin-left: auto;
        background: linear-gradient(135deg, #0b5f85, #01324a);
        border-bottom-right-radius: 4px;
        text-align: left;
    }
    /* Bot bubble */
    .message.bot {
        margin-right: auto;
        background: rgba(255,255,255,0.08);
        border:1px solid rgba(255,255,255,0.12);
        border-bottom-left-radius:4px;
        color:rgba(255,255,255,0.85);
    }
    /* Chat message spacing */
    .marker-chat-messages {
        display:block;
    }
    /* Chat Input - Theme Friendly */
    div[data-testid="stChatInput"] {
        position:sticky;
        bottom:15px;
        padding-top:10px;
        z-index:999;
    }
    div[data-testid="stChatInput"] textarea {
        border-radius:20px;
        color:#000;
    }
    
    /* Footer */
    .footer {
        text-align:center;
        color:#777;
        margin-top:40px;
    }
    /* ── Chat header ── */
    .chat-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 14px;
        padding: 0 2px;
    }
    .chat-header .avatar {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
    }
    .chat-header .name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 16px;
        color: #fff;
        line-height: 1.2;
    }
    .chat-header .sub {
        font-size: 13px;
        color: rgba(255,255,255,0.55);
        display: flex;
        align-items: center;
        gap: 6px;
        margin-top: 2px;
    }
    .chat-header .dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #4ADE80;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(74,222,128,0.55);
        animation: livePulse 2s infinite;
    }
    /* ── Tagged containers ── */
    .tag-chat-messages {
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 16px !important;
        background: rgba(0,0,0,0.18) !important;
        padding: 12px 16px !important;
        margin-bottom: 12px !important;
    }
    .tag-chat-input {
        margin-top: 4px;
    }
    .tag-lead-form {
        margin-top: 8px;
    }
    /* Lead form helpers */
    .lead-form-note {
        font-size: 14px;
        color: rgba(255,255,255,0.65);
        margin: 0 0 12px 0;
        text-align: center;
    }
    .lead-success {
        background: rgba(74,222,128,0.12);
        border: 1px solid rgba(74,222,128,0.35);
        border-radius: 12px;
        padding: 14px 18px;
        color: #4ADE80;
        font-size: 14px;
        text-align: center;
        margin-top: 12px;
    }
    /* ── Form input styling ── */
    div[data-testid="stForm"] {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    /* Hide Streamlit's "Press Enter to submit form" helper text */
    div[data-testid="stForm"] [data-testid="InputInstructions"],
    div[data-testid="stForm"] small,
    div[data-testid="stForm"] [data-testid="stFieldInstructions"] {
        display: none !important;
    }
    /* Custom Base Input Styling */
    div[data-testid="stForm"] [data-testid="stTextInput"] input,
    div[data-testid="stForm"] [data-testid="stTextArea"] textarea {
        background: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        color: #111 !important;
        padding: 12px 18px !important;
        font-size: 14px !important;
        outline: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stForm"] [data-testid="stTextInput"] input::placeholder,
    div[data-testid="stForm"] [data-testid="stTextArea"] textarea::placeholder {
        color: rgba(0,0,0,0.45) !important;
    }
    /* Remove Red Focus Highlight & Replace with Soft Azure Glow */
    div[data-testid="stForm"] [data-testid="stTextInput"] input:focus,
    div[data-testid="stForm"] [data-testid="stTextArea"] textarea:focus,
    div[data-testid="stForm"] [data-baseweb="input"]:focus-within {
        border-color: rgba(11, 95, 133, 0.8) !important;
        box-shadow: 0 0 8px rgba(11, 95, 133, 0.4) !important;
        outline: none !important;
    }
    /* ── Force chat form columns to stay side-by-side on mobile ── */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 8px !important;
        align-items: center !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div {
        min-width: 0 !important;          /* allow input to shrink */
    }
    /* Input column takes remaining space */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div:first-child {
        flex: 1 1 auto !important;
    }
    /* Button column stays fixed width */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div:last-child {
        flex: 0 0 48px !important;
        width: 48px !important;
        max-width: 48px !important;
    }
    /* Chat send button */
    div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
        border-radius: 50% !important;
        width: 44px !important;
        height: 44px !important;
        min-width: 44px !important;
        padding: 0 !important;
        background: linear-gradient(135deg, #0b5f85, #01324a) !important;
        border: none !important;
        color: #fff !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    /* Lead submit button */
    .lead-form-button-fix button {
        border-radius: 24px !important;
        width: 100% !important;
        height: 42px !important;
        min-width: 100% !important;
        padding: 0 24px !important;
        background: linear-gradient(135deg, #0b5f85, #01324a) !important;
        border: none !important;
        color: #fff !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    /* Chat input remove red border */
    div[data-testid="stTextInput"] *,
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] div[data-baseweb="base-input"],
    div[data-testid="stTextInput"] input {
        border-color: rgba(255,255,255,0.12) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {
        border-color: rgba(11,95,133,0.8) !important;
        box-shadow: 0 0 8px rgba(11,95,133,0.4) !important;
    }
    .lede,
    .lede.secondary {
        text-align: center !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    .stMarkdown:has(.lede),
    .stMarkdown:has(.lede.secondary) {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lead_form_shown" not in st.session_state:
    st.session_state.lead_form_shown = False
if "show_lead_form_now" not in st.session_state:
    st.session_state.show_lead_form_now = False
if "lead_submitted" not in st.session_state:
    st.session_state.lead_submitted = False
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "pending_bot" not in st.session_state:
    st.session_state.pending_bot = False
if "db_ready" not in st.session_state:
    try:
        db_connection, cursor = database_connection()
        table_creation(db_connection, cursor)
    except Exception:
        logger.exception("Database initialization failed")
        st.error("The lead database could not be initialized.")
    st.session_state.db_ready = True
FALLBACK_MARKER = "please leave your details below"

# --------------------------------
# Hero
# --------------------------------
st.markdown(
    """
<div class="eyebrow"><span><span class="pulse-dot"></span> AI Dental Clinic Assistant Demo</span></div>
<h1 class="hero-title">See How AI Can Help You Capture More Patients &amp; Support Them 24/7</h1>
<p class="lede">Give your potential patients instant answers while capturing valuable lead information — even when your team is unavailable.</p>
<p class="lede secondary">This AI-powered chatbot is designed for dental clinics to handle common patient questions, guide visitors through their care options, and help you identify serious prospects faster.</p>
<div class="features-heading">What This Demo Shows</div>
""",
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
            </div>
            <h3>Instant Patient Support</h3>
            <p>Answer frequently asked dental questions anytime with an AI assistant that provides quick, helpful responses.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon">
                <svg width="18" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></svg>
            </div>
            <h3>Smart Lead Capture</h3>
            <p>Collect visitor details and understand their needs so your team can follow up with qualified patients.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="icon">
                <svg width="18" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/></svg>
            </div>
            <h3>Always Available</h3>
            <p>Never miss an opportunity. Your AI assistant works around the clock to engage website visitors and support your clinic.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown(
    """
<div class="demo-cta">
    <h2>Try the Demo Below</h2>
    <p>Experience how an AI chatbot can turn more website visitors into potential patients while saving your team valuable time.</p>
    <div class="demo-arrow">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
st.divider()
# ──────────────────────────────────────────────────────────────────────────
# Chat card
# ──────────────────────────────────────────────────────────────────────────
left, center, right = st.columns([1.8, 3, 1.8])
with center:
    # Header
    st.markdown(
        """
        <div class="chat-header">
            <div class="avatar">🦷</div>
            <div>
                <div class="name">Dental Clinic Assistant</div>
                <div class="sub">
                    <span class="dot"></span> Online now
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="marker-chat-messages"></div>',
        unsafe_allow_html=True
    )
    messages_area = st.container(height=450)
    with messages_area:
        bubbles = "".join(
            f'<div class="message {m["type"]}">{m["text"]}</div>'
            for m in st.session_state.messages
        )
        st.markdown(
            bubbles,
            unsafe_allow_html=True
        )
        if st.session_state.pending_bot:
            st.markdown(
                '<div class="message bot">Thinking…</div>',
                unsafe_allow_html=True
            )
        # Lead form inside conversation area
        if (
            st.session_state.show_lead_form_now
            and not st.session_state.lead_submitted
        ):
            st.markdown(
                '<div class="marker-lead-form"></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                """
                <p class="lead-form-note">
                Want us to get back to you directly? Leave your details below.
                </p>
                """,
                unsafe_allow_html=True
            )
            st.markdown(
                '<div class="lead-form-button-fix">',
                unsafe_allow_html=True
            )
            with st.form(
                "lead_form",
                clear_on_submit=False
            ):
                name = st.text_input(
                    "Your name",
                    placeholder="Your name",
                    label_visibility="collapsed",
                )
                email = st.text_input(
                    "Your email",
                    placeholder="Your email",
                    label_visibility="collapsed",
                )
                extra = st.text_area(
                    "Anything else",
                    placeholder="Anything else (optional)",
                    label_visibility="collapsed",
                    height=70,
                )
                submitted = st.form_submit_button(
                    "Submit"
                )
                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )
            if submitted:
                if not name.strip() or not email.strip():
                    st.warning(
                        "Please enter your name and email."
                    )
                else:
                    # Wrapped in try/except: if the DB insert or notification
                    # fails (bad connection, schema mismatch, etc.) the user
                    # now sees a clear error instead of the whole app crashing.
                    try:
                        notifier(
                            name=name.strip(),
                            email=email.strip(),
                            question=st.session_state.last_question,
                            message=extra.strip() or None,
                        )
                    except Exception as e:
                        st.error(f"Something went wrong saving your details: {e}")
                    else:
                        st.session_state.lead_submitted = True
                        st.rerun()
        if st.session_state.lead_submitted:
            st.markdown(
                """
                <div class="lead-success">
                Thanks! We've received your details and will get back to you soon.
                </div>
                """,
                unsafe_allow_html=True
            )
    # Generate bot reply
    if st.session_state.pending_bot:
        last_user = st.session_state.last_question
        try:
            response, show_form = full_pipeline(
                last_user,
                st.session_state.messages,
            )
            if "[[LEAD_FORM]]" in response:
                st.session_state.show_lead_form_now = True
                response = response.replace("[[LEAD_FORM]]", "").strip()
        except Exception:
            logger.exception("Frontend pipeline call failed")
            response = (
                "I don't have that information right now."
            )
            show_form = False
        st.session_state.messages.append(
            {
                "type": "bot",
                "text": response
            }
        )
        st.session_state.pending_bot = False
        if (
            FALLBACK_MARKER in response.lower()
            or show_form
        ):
            st.session_state.show_lead_form_now = True
        st.rerun()
    # Chat input stays at bottom
    st.markdown(
        '<div class="marker-chat-input"></div>',
        unsafe_allow_html=True
    )
    with st.form(
        "chat_form",
        clear_on_submit=True
    ):
        col_input, col_btn = st.columns([6, 1])
        query = col_input.text_input(
            "Message",
            placeholder="Ask about treatments, appointments, pricing...",
            label_visibility="collapsed",
            key="chat_input",
        )
        sent = col_btn.form_submit_button(
            "➤"
        )
    if sent and query.strip():
        st.session_state.last_question = query.strip()
        st.session_state.messages.append(
            {
                "type": "user",
                "text": query.strip()
            }
        )
        st.session_state.pending_bot = True
        st.rerun()
# Tag Streamlit containers so the CSS classes apply correctly
components.html(
    """
    <script>
    (function () {
        const markerToTag = {
            "marker-chat-messages": "tag-chat-messages",
            "marker-chat-input": "tag-chat-input",
            "marker-lead-form": "tag-lead-form",
        };
        function tagAncestors() {
            const doc = window.parent.document;
            Object.entries(markerToTag).forEach(([markerClass, tagClass]) => {
                const marker = doc.querySelector("." + markerClass);
                if (!marker) return;
                let el = marker.parentElement;
                while (el && el.getAttribute("data-testid") !== "stVerticalBlock") {
                    el = el.parentElement;
                }
                if (el && !el.classList.contains(tagClass)) {
                    el.classList.add(tagClass);
                }
            });
        }
        let tries = 0;
        const timer = setInterval(function () {
            tagAncestors();
            tries += 1;
            if (tries > 25) clearInterval(timer);
        }, 150);
    })();
    </script>
    """,
    height=0,
)