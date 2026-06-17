import streamlit as st
from pathlib import Path
import os
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FileVault · File Manager",
    page_icon="🗂️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* ── Reset / base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0a0a0f;
    color: #e8e6f0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 720px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 2.5rem 2rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #f1f0ff;
    line-height: 1.1;
    margin: 0 0 0.5rem;
}
.hero-sub {
    font-size: 0.95rem;
    color: #9896b8;
}

/* ── Operation cards ── */
.op-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin-bottom: 2rem;
}
.op-card {
    background: #131320;
    border: 1.5px solid #222240;
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
}
.op-card:hover { border-color: #6366f1; background: #1a1a35; }
.op-card.active { border-color: #6366f1; background: #1e1e42; }
.op-icon { font-size: 1.6rem; margin-bottom: 0.3rem; }
.op-name { font-size: 0.78rem; font-weight: 600; color: #ccc8f0; }

/* ── Panel ── */
.panel {
    background: #131320;
    border: 1px solid #222240;
    border-radius: 14px;
    padding: 1.75rem 1.75rem;
    margin-bottom: 1.5rem;
}
.panel-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f0ff;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0e0e1c !important;
    border: 1.5px solid #2a2a4a !important;
    border-radius: 8px !important;
    color: #e8e6f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* ── Radio as tabs ── */
.stRadio > div {
    flex-direction: row !important;
    gap: 0.5rem;
}
.stRadio label {
    background: #1a1a2e;
    border: 1.5px solid #2a2a4a;
    border-radius: 8px;
    padding: 0.4rem 1rem;
    font-size: 0.83rem;
    color: #9896b8;
    cursor: pointer;
}
.stRadio label[data-checked="true"] {
    border-color: #6366f1;
    color: #f1f0ff;
    background: #1e1e42;
}

/* ── Buttons ── */
.stButton > button {
    background: #6366f1 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.5rem !important;
    transition: background 0.2s, transform 0.1s !important;
}
.stButton > button:hover {
    background: #4f46e5 !important;
    transform: translateY(-1px) !important;
}

/* ── Success / error / info boxes ── */
.stSuccess, .stError, .stInfo, .stWarning {
    border-radius: 8px !important;
    font-size: 0.88rem !important;
}

/* ── File content display ── */
.file-content {
    background: #080810;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #a8a6d0;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 260px;
    overflow-y: auto;
    line-height: 1.6;
}

/* ── File stat pills ── */
.stat-row { display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap; }
.stat-pill {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #8886b0;
}
.stat-pill span { color: #c8c6f0; font-weight: 500; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #1e1e3a; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">// Python Project</div>
    <div class="hero-title">FileVault</div>
    <div class="hero-sub">Create, read, update, and delete files — straight from your browser.</div>
</div>
""", unsafe_allow_html=True)


# ── Operation selector ────────────────────────────────────────────────────────
ops = {
    "➕ Create": "create",
    "📖 Read": "read",
    "✏️ Update": "update",
    "🗑️ Delete": "delete",
}

col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]
labels = list(ops.keys())

if "operation" not in st.session_state:
    st.session_state.operation = "create"

for i, (label, key) in enumerate(ops.items()):
    with cols[i]:
        active_style = "border: 1.5px solid #6366f1; background: #1e1e42;" if st.session_state.operation == key else ""
        if st.button(label, key=f"btn_{key}", use_container_width=True):
            st.session_state.operation = key

operation = st.session_state.operation

st.markdown("<hr class='divider'>", unsafe_allow_html=True)


# ── CREATE ────────────────────────────────────────────────────────────────────
if operation == "create":
    st.markdown('<div class="panel-title">➕ &nbsp;Create a new file</div>', unsafe_allow_html=True)

    filepath = st.text_input("File path", placeholder="e.g. notes/hello.txt", key="create_path")
    content  = st.text_area("File content", placeholder="Type what you want to write...", height=160, key="create_content")

    if st.button("Create file", key="do_create"):
        if not filepath.strip():
            st.error("Enter a file path first.")
        else:
            path = Path(filepath.strip())
            if path.exists():
                st.error(f"**{path}** already exists. Choose a different name.")
            else:
                try:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                    st.success(f"**{path}** created successfully — {len(content)} characters written.")
                except Exception as e:
                    st.error(f"Could not create file: {e}")


# ── READ ──────────────────────────────────────────────────────────────────────
elif operation == "read":
    st.markdown('<div class="panel-title">📖 &nbsp;Read a file</div>', unsafe_allow_html=True)

    filepath = st.text_input("File path", placeholder="e.g. notes/hello.txt", key="read_path")

    if st.button("Open file", key="do_read"):
        if not filepath.strip():
            st.error("Enter a file path first.")
        else:
            path = Path(filepath.strip())
            if not path.exists():
                st.error(f"No file found at **{path}**.")
            else:
                try:
                    content = path.read_text(errors="replace")
                    size_kb = path.stat().st_size / 1024
                    lines   = content.count("\n") + 1
                    chars   = len(content)

                    st.markdown(f"""
                    <div class="stat-row">
                        <div class="stat-pill">Size &nbsp;<span>{size_kb:.2f} KB</span></div>
                        <div class="stat-pill">Lines &nbsp;<span>{lines}</span></div>
                        <div class="stat-pill">Chars &nbsp;<span>{chars}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f'<div class="file-content">{content if content else "<em style=\'color:#555\'>Empty file</em>"}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Could not read file: {e}")


# ── UPDATE ────────────────────────────────────────────────────────────────────
elif operation == "update":
    st.markdown('<div class="panel-title">✏️ &nbsp;Update a file</div>', unsafe_allow_html=True)

    filepath = st.text_input("File path", placeholder="e.g. notes/hello.txt", key="update_path")
    action   = st.radio("What to do", ["Rename", "Append content", "Overwrite content"], key="update_action", horizontal=True)

    if action == "Rename":
        new_name = st.text_input("New file path", placeholder="e.g. notes/renamed.txt", key="new_name")
        if st.button("Rename file", key="do_rename"):
            if not filepath.strip():
                st.error("Enter the current file path.")
            elif not new_name.strip():
                st.error("Enter the new file path.")
            else:
                path = Path(filepath.strip())
                new_path = Path(new_name.strip())
                if not path.exists():
                    st.error(f"**{path}** does not exist.")
                elif new_path.exists():
                    st.error(f"**{new_path}** already exists.")
                else:
                    try:
                        path.rename(new_path)
                        st.success(f"Renamed **{path}** → **{new_path}**")
                    except Exception as e:
                        st.error(f"Rename failed: {e}")

    elif action == "Append content":
        extra = st.text_area("Text to append", height=130, key="append_text")
        if st.button("Append", key="do_append"):
            if not filepath.strip():
                st.error("Enter a file path first.")
            else:
                path = Path(filepath.strip())
                if not path.exists():
                    st.error(f"**{path}** does not exist.")
                else:
                    try:
                        with open(path, "a") as f:
                            f.write("\n" + extra)
                        st.success(f"Appended {len(extra)} characters to **{path}**.")
                    except Exception as e:
                        st.error(f"Append failed: {e}")

    else:  # Overwrite
        new_content = st.text_area("New content (replaces everything)", height=160, key="overwrite_text")
        if st.button("Overwrite", key="do_overwrite"):
            if not filepath.strip():
                st.error("Enter a file path first.")
            else:
                path = Path(filepath.strip())
                if not path.exists():
                    st.error(f"**{path}** does not exist.")
                else:
                    try:
                        path.write_text(new_content)
                        st.success(f"**{path}** overwritten — {len(new_content)} characters written.")
                    except Exception as e:
                        st.error(f"Overwrite failed: {e}")


# ── DELETE ────────────────────────────────────────────────────────────────────
elif operation == "delete":
    st.markdown('<div class="panel-title">🗑️ &nbsp;Delete a file</div>', unsafe_allow_html=True)

    filepath = st.text_input("File path", placeholder="e.g. notes/hello.txt", key="delete_path")

    if "confirm_delete" not in st.session_state:
        st.session_state.confirm_delete = False

    if filepath.strip():
        path = Path(filepath.strip())
        if path.exists():
            size_kb = path.stat().st_size / 1024
            st.warning(f"**{path}** · {size_kb:.2f} KB — this cannot be undone.")
            confirm = st.checkbox("Yes, permanently delete this file", key="delete_confirm")
            if confirm:
                if st.button("Delete file", key="do_delete"):
                    try:
                        path.unlink()
                        st.success(f"**{path}** has been deleted.")
                        st.session_state.delete_confirm = False
                    except Exception as e:
                        st.error(f"Delete failed: {e}")
        else:
            if st.button("Check file", key="do_delete_check"):
                st.error(f"No file found at **{path}**.")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'IBM Plex Mono',monospace; font-size:0.72rem; color:#444466;">
    FileVault &nbsp;·&nbsp; Built with Python &amp; Streamlit
</div>
""", unsafe_allow_html=True)