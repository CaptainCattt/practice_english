import streamlit as st
import json
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Verb Practice",
    page_icon="📘",
    layout="centered"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
/* Remove extra Streamlit padding */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1rem;
}

/* HEADER */
.header-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 6px 0 14px 0;
    text-align: center;
         margin-top: 24px;      
}
.header-title {
    font-size: 48px;
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-sub {
    font-size: 15px;
    color: #6b7280;
    margin-top: 4px;
}
.header-line {
    width: 70px;
    height: 3px;
    background-color: #e5e7eb;
    margin-top: 8px;
    border-radius: 999px;
}

/* VERB */
.verb {
    font-size: 38px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 4px;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* MEANING */
.meaning {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
    margin: 8px 0 12px 0;
}

/* EXAMPLE BOX */
.example {
    background: #f0f4ff;
    padding: 10px 12px;
    border-radius: 12px;
    margin-top: 10px;
    font-size: 15px;
}

/* BUTTON CENTER */
.stButton > button {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------


@st.cache_data
def load_data():
    with open("Data.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_user_example(verbs, current_verb, sentence):
    for v in verbs:
        if v["v1"] == current_verb["v1"]:
            if "user_examples" not in v:
                v["user_examples"] = []
            v["user_examples"].append(sentence)
            break

    with open("Data.json", "w", encoding="utf-8") as f:
        json.dump(verbs, f, ensure_ascii=False, indent=2)


def reset_form():
    st.session_state.v2_input = ""
    st.session_state.v3_input = ""
    st.session_state.user_sentence = ""


verbs = load_data()

# ---------------- SESSION ----------------
if "verb" not in st.session_state:
    st.session_state.verb = random.choice(verbs)
    st.session_state.result = None

verb = st.session_state.verb

# ---------------- HEADER ----------------
st.markdown("""
<div class="header-box">
    <div class="header-title">Verb Practice For MeoCon</div>
    <div class="header-sub">🚀 Practice V2 & V3 every day 🚀</div>
    <div class="header-line"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- VERB & MEANING ----------------
st.markdown(f"<div class='verb'>{verb['v1']}</div>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        margin: 15px 0;
    ">
        📖 {verb['meaning']} 📖
    </div>
    """,
    unsafe_allow_html=True
)
if "form_id" not in st.session_state:
    st.session_state.form_id = 0

with st.form(f"answer_form_{st.session_state.form_id}"):
    col1, col2 = st.columns(2)
    with col1:
        v2_input = st.text_input(
            "✏️ V2 / V-ed",
            key=f"v2_{st.session_state.form_id}"
        )
    with col2:
        v3_input = st.text_input(
            "✏️ V3",
            key=f"v3_{st.session_state.form_id}"
        )

    submitted = st.form_submit_button("✅ Check")


# ---------------- CHECK LOGIC ----------------
if submitted:
    if (
        v2_input.strip().lower() == verb["v2"]
        and v3_input.strip().lower() == verb["v3"]
    ):
        st.session_state.result = "correct"
    else:
        st.session_state.result = "wrong"

# ---------------- RESULT ----------------
if st.session_state.result == "correct":
    st.success("🎉 Correct! Great job!")

    st.markdown(
        f"""
        <div class="example">
            <b>📌 Example</b><br>
            {verb['example']}<br>
            <i>{verb['example_meaning']}</i>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("### ✍️ Your own sentence")
    if "user_examples" in verb and len(verb["user_examples"]) > 0:
        st.markdown("### 📚 Your saved sentences")
        for i, s in enumerate(verb["user_examples"], 1):
            st.markdown(f"**{i}.** {s}")

    user_sentence = st.text_area(
        "Write your sentence using this verb",
        placeholder="Example: I became more confident after practicing every day.",
        height=80
    )
    if st.button("💾 Save my sentence"):
        if user_sentence.strip() == "":
            st.warning("⚠️ Please write a sentence first.")
        else:
            save_user_example(verbs, verb, user_sentence.strip())
            st.success("✅ Saved! Your sentence has been recorded.")

    st.markdown("<div class='next-btn'>", unsafe_allow_html=True)

    if st.button("🔄 Next verb"):
        st.session_state.form_id += 1
        st.session_state.verb = random.choice(verbs)
        st.session_state.result = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.result == "wrong":
    st.error("❌ Not correct")

    st.markdown(
        f"""
        <div class="example">
            ✔️ <b>V2:</b> {verb['v2']}<br>
            ✔️ <b>V3:</b> {verb['v3']}<br><br>
            <b>📌 Example</b><br>
            {verb['example']}<br>
            <i>{verb['example_meaning']}</i>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div class='retry-btn'>", unsafe_allow_html=True)

    if st.button("🔄 Let's try another verb"):
        st.session_state.form_id += 1
        st.session_state.verb = random.choice(verbs)
        st.session_state.result = None
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
