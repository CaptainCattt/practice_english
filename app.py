import streamlit as st
import json
import random

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="English Practice App",
    page_icon="📘",
    layout="centered"
)

# ==================================================
# LOAD DATA
# ==================================================


@st.cache_data
def load_verbs():
    with open("Data.json", "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def load_comparisons():
    with open("comparison_data.json", "r", encoding="utf-8") as f:
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


verbs = load_verbs()
comparison_items = load_comparisons()["data"]

# ==================================================
# GLOBAL STYLE (GIỮ PHONG CÁCH CŨ)
# ==================================================
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }

.header-title {
    font-size: 44px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub { text-align:center; color:#6b7280; margin-bottom:14px; }

.word {
    font-size: 36px;
    font-weight: 800;
    text-align: center;
}
.meaning {
    text-align: center;
    font-size: 22px;
    font-weight: 700;
}
.example {
    background: #f0f4ff;
    padding: 12px;
    border-radius: 12px;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc, #eef2ff);
    padding-top: 1.2rem;
}

/* App title */
.sidebar-title {
    font-size: 22px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 4px;
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.sidebar-sub {
    text-align: center;
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 14px;
}

/* Radio group spacing */
div[role="radiogroup"] {
    gap: 8px;
}

/* Radio button style */
div[role="radiogroup"] > label {
    background: white;
    padding: 10px 14px;
    border-radius: 14px;
    font-weight: 600;
    border: 1px solid #e5e7eb;
    transition: all 0.2s ease;
}

/* Hover */
div[role="radiogroup"] > label:hover {
    background: #eef2ff;
    border-color: #6366f1;
}

/* Selected */
div[role="radiogroup"] > label[data-checked="true"] {
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white;
    border: none;
}

/* Footer */
.sidebar-footer {
    margin-top: 22px;
    text-align: center;
    font-size: 12px;
    color: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# HEADER
# ==================================================
st.markdown("<div class='header-title'>English Practice For MeoCon</div>",
            unsafe_allow_html=True)
st.markdown("<div class='sub'>V2–V3 • Comparison • Theory</div>",
            unsafe_allow_html=True)

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Lý thuyết"
# ==================================================
# TABS
# ==================================================
with st.sidebar:
    st.markdown("<div class='sidebar-title'>📘 English Practice</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Learn smarter every day</div>",
                unsafe_allow_html=True)

    st.radio(
        label="",
        options=[
            "Lý thuyết",
            "Học bài - Luyện tập",
            "V2 - V3",
            "So sánh"
        ],
        key="current_tab"
    )

    st.markdown(
        "<div class='sidebar-footer'>© 2026 | MeoCon App</div>",
        unsafe_allow_html=True
    )

# ==================================================
# 📘 THEORY TAB
# ==================================================


def render_section(section):
    # Heading
    st.markdown(
        f"<div style='font-size:20px;font-weight:700;margin-bottom:6px;color:black;'>🔹 {section['heading']}</div>",
        unsafe_allow_html=True
    )

    # Nội dung chữ
    if "content" in section:
        for c in section["content"]:
            st.markdown(f"- {c}")

    # Rules / Uses / Lists khác
    for key in ["rules", "uses", "time_signals", "irregular", "common_verbs"]:
        if key in section:
            st.markdown(f"**📌 {key.replace('_', ' ').title()}**")
            for r in section[key]:
                st.markdown(f"- {r}")

    # Examples
    if "examples" in section:
        st.markdown(
            "<div style='background:#f1f5f9;padding:5px;border-radius:8px;margin-bottom:10px;color:black;'>",
            unsafe_allow_html=True
        )
        for ex in section["examples"]:
            if isinstance(ex, dict):
                st.markdown(f"**EN:** {ex['en']}")
                st.markdown(f"**VI:** {ex['vi']}")
                st.markdown("---")
            else:
                st.markdown(f"- {ex}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


def load_theory(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


if st.session_state.current_tab == "Lý thuyết":

    verb_data = load_theory("theory_verb_v2_v3.json")
    compare_data = load_theory("theory_comparison_full.json")

    # ===============================
    # 📘 V2 – V3
    # ===============================
    st.markdown(
        f"<h2 style='color:black;'>📘 {verb_data['title']}</h2>",
        unsafe_allow_html=True
    )

    for section in verb_data["sections"]:
        render_section(section)

    st.divider()

    # ===============================
    # 📊 COMPARISON
    # ===============================
    st.markdown(
        f"<h2 style='color:black;'>📊 {compare_data['title']}</h2>",
        unsafe_allow_html=True
    )

    for section in compare_data["sections"]:
        render_section(section)


if st.session_state.current_tab == "Học bài - Luyện tập":
    st.markdown("## 📖 HỌC BÀI – XEM TOÀN BỘ DỮ LIỆU")
    st.caption("👉 Xem kỹ toàn bộ từ vựng và ví dụ trước khi luyện tập")

    tab_verb, tab_compare = st.tabs(
        ["📘 Verb V2 – V3", "📊 So sánh hơn / nhất"]
    )
    with tab_verb:
        for i, v in enumerate(verbs, 1):
            with st.container(border=True):
                st.markdown(f"### {i}. {v['v1']} – {v['v2']} – {v['v3']}")
                st.markdown(f"📘 **Nghĩa:** {v['meaning']}")
                st.markdown(f"📌 *{v['example']}*")
                st.caption(v['example_meaning'])

    with tab_compare:
        for i, item in enumerate(comparison_items, 1):
            with st.container(border=True):
                st.markdown(f"### {i}. {item['base']}")

                st.markdown(f"**📖 Nghĩa:** {item['meaning']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"🔹 **So sánh hơn:** {item['comparative']}")
                with col2:
                    st.markdown(f"🔹 **So sánh nhất:** {item['superlative']}")

                st.markdown(f"📌 *{item['example']}*")


# ✏️ VERB PRACTICE TAB (FIX CHUẨN)
if st.session_state.current_tab == "V2 - V3":

    if "verb" not in st.session_state:
        st.session_state.verb = random.choice(verbs)
        st.session_state.verb_result = None
        st.session_state.form_id = 0

    verb = st.session_state.verb

    st.markdown(
        f"<div class='word'>{verb['v1']}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='meaning'>📖 {verb['meaning']} 📖</div>", unsafe_allow_html=True)

    with st.form(f"verb_form_{st.session_state.form_id}"):
        c1, c2 = st.columns(2)
        v2 = c1.text_input("✏️ V2")
        v3 = c2.text_input("✏️ V3")
        submit = st.form_submit_button("✅ Check")

    if submit:
        if v2.strip().lower() == verb["v2"] and v3.strip().lower() == verb["v3"]:
            st.session_state.verb_result = "correct"
        else:
            st.session_state.verb_result = "wrong"

    # ================= RESULT =================
    if st.session_state.verb_result == "correct":
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
            if user_sentence.strip():
                save_user_example(verbs, verb, user_sentence.strip())
                st.success("✅ Saved!")
            else:
                st.warning("⚠️ Please write a sentence first.")

        if st.button("🔄 Next verb"):
            st.session_state.form_id += 1
            st.session_state.verb = random.choice(verbs)
            st.session_state.verb_result = None
            st.rerun()

    elif st.session_state.verb_result == "wrong":
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

        if st.button("🔄 Try another verb"):
            st.session_state.form_id += 1
            st.session_state.verb = random.choice(verbs)
            st.session_state.verb_result = None
            st.rerun()

# 📊 COMPARISON PRACTICE TAB (UI IMPROVED)
if st.session_state.current_tab == "So sánh":

    if "compare_item" not in st.session_state:
        st.session_state.compare_item = random.choice(comparison_items)
        st.session_state.compare_mode = random.choice(
            ["comparative", "superlative"])
        st.session_state.compare_result = None

    item = st.session_state.compare_item
    mode = st.session_state.compare_mode

    # ---------- WORD ----------
    st.markdown(
        f"""
        <div style="
            font-size:36px;
            font-weight:800;
            text-align:center;
            color:#000000;
            margin: 10px 5px;
        ">
            {item['base']}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:20px;
            font-weight:700;
            margin-bottom: 20px;
        ">
            📖 {item['meaning']} 📖
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- MODE BADGE ----------
    badge_color = "#2563eb" if mode == "comparative" else "#7c3aed"
    badge_text = "Comparative" if mode == "comparative" else "Superlative"

    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:14px;">
            <span style="
                background:{badge_color};
                color:white;
                padding:6px 14px;
                border-radius:999px;
                font-weight:700;
                font-size:14px;
            ">
                {badge_text}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- FORM ----------
    with st.form("compare_form"):
        ans = st.text_input(
            "✏️ Nhập dạng đúng",
            placeholder="Type the correct form here..."
        )
        submit = st.form_submit_button("✅ Check")

    # ---------- CHECK ----------
    if submit:
        if ans.strip().lower() == item[mode].lower():
            st.session_state.compare_result = "correct"
        else:
            st.session_state.compare_result = "wrong"

    # ---------- RESULT ----------
    if st.session_state.compare_result == "correct":
        st.success("🎉 Correct! Well done!")

    elif st.session_state.compare_result == "wrong":
        st.error(f"❌ Correct answer: **{item[mode]}**")

    # ---------- EXAMPLE + NEXT ----------
    if st.session_state.compare_result:

        st.markdown(
            f"""
            <div style="
                background:#ecfeff;
                padding:14px;
                border-radius:14px;
                margin-top:14px;
                font-size:15px;
            ">
                <b>📌 Example</b><br>
                {item['example']}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔄 Next word"):
            st.session_state.compare_item = random.choice(comparison_items)
            st.session_state.compare_mode = random.choice(
                ["comparative", "superlative"])
            st.session_state.compare_result = None
            st.rerun()
