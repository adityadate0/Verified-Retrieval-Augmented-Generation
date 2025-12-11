import streamlit as st
import requests
import json
import time

# --- CONFIGURATION ---
API_URL = "http://localhost:8000"
st.set_page_config(page_title="Veri-RAG Enterprise", layout="wide", page_icon="🧠")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* 1. Main Background adapting to theme */
    
    /* 2. Card Styling */
    .stInfo, .stSuccess, .stError, .stWarning {
        background-color: var(--secondary-background-color); 
        border: 1px solid var(--text-color);
        border-radius: 12px;
        opacity: 0.9;
    }
    
    /* 3. Text Colors */
    .stMarkdown p {
        color: var(--text-color) !important;
    }
    
    /* 4. Remove default top padding */
    .block-container {
        padding-top: 3rem;
    }
    
    /* 5. Title Styling */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        /* Default theme color for visibility */
    }
    
    /* 6. Chat Input - Fixed to Bottom */
    .stChatInput {
        position: fixed;
        bottom: 30px;
        z-index: 100;
    }

    /* 7. Process Step Cards (For "How it Works") */
    .step-card {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--text-color);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        height: 100%;
    }
    .arrow {
        text-align: center;
        font-size: 2em;
        font-weight: bold;
        color: var(--text-color);
        padding: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=50)
    st.header("🗂️ Data Ingestion")
    uploaded_file = st.file_uploader("Upload Policy/Manual (PDF)", type="pdf")
    
    if uploaded_file:
        if st.button("🚀 Upload & Vectorize", type="primary"):
            files = {"file": uploaded_file}
            with st.spinner("Encrypting & Vectorizing..."):
                try:
                    requests.post(f"{API_URL}/upload", files=files, timeout=30)
                    requests.post(f"{API_URL}/ingest", timeout=600) 
                    st.toast("Document Indexed Successfully!", icon="✅")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
    
    if st.button("⚡ Index Knowledge", type="secondary"):
        with st.spinner("Processing..."):
            try:
                requests.post(f"{API_URL}/ingest", timeout=600)
                st.success("Knowledge Base Updated!")
            except:
                st.error("Backend Offline")
    
    st.divider()
    
    # --- NEW STOP BUTTON ---
    # This button forces a rerun, effectively cancelling a stuck loop on the next UI tick.
    if st.button("⛔ Stop / Reset", type="primary"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### ⚙️ Neural Status")
    try:
        if requests.get(f"{API_URL}/docs", timeout=2).status_code == 200:
             st.success("🟢 Backend API: **Online**")
        else:
             st.error("🔴 Backend API: **Offline**")
    except:
        st.error("🔴 Backend API: **Unreachable**")


# --- MAIN CONTENT ---

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. HERO SECTION & HOW IT WORKS (Only show if no chat history)
if not st.session_state.messages:
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("https://img.icons8.com/fluency/96/brain.png", width=80)
    with col2:
        st.title("Veri-RAG Engine")
        st.markdown("#### Secure Enterprise Knowledge Retrieval & Compliance Verification")
    
    st.divider()
    
    # --- NEW "HOW IT WORKS" SECTION ---
    st.markdown("### 🧠 How the Neural Engine Works")
    st.markdown("This system uses a **Multi-Agent Architecture** to ensure zero hallucinations.")
    
    # Row 1: Diagram
    c1, c2, c3, c4, c5 = st.columns([1, 0.2, 1, 0.2, 1])
    
    with c1:
        st.markdown("""
        <div class="step-card">
            <h3>🔍 Step 1</h3>
            <p><strong>Retrieval</strong></p>
            <p style="font-size:0.8em">Scans the Vector Database to find exact PDF pages matching your query.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown("<div class='arrow'>→</div>", unsafe_allow_html=True)
        
    with c3:
        st.markdown("""
        <div class="step-card">
            <h3>👨‍💻 Step 2</h3>
            <p><strong>Analyst Agent</strong></p>
            <p style="font-size:0.8em">Drafts a comprehensive answer based <em>only</em> on the retrieved facts.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c4:
        st.markdown("<div class='arrow'>→</div>", unsafe_allow_html=True)
        
    with c5:
        st.markdown("""
        <div class="step-card">
            <h3>👮 Step 3</h3>
            <p><strong>Auditor Agent</strong></p>
            <p style="font-size:0.8em">Reviews the draft for hallucinations and compliance violations.</p>
        </div>
        """, unsafe_allow_html=True)

    # Row 2: Final Output Arrow
    st.markdown("<div style='text-align: center; font-size: 2em; color: var(--text-color);'>↓</div>", unsafe_allow_html=True)
    
    # Row 3: Final Output
    c_final_1, c_final_2, c_final_3 = st.columns([1, 2, 1])
    with c_final_2:
        st.markdown("""
        <div class="step-card" style="border-color: #4776E6;">
            <h3 style="color: #4776E6;">📝 Step 4: Final Synthesis</h3>
            <p>The <strong>Chief Editor</strong> merges the Draft and Audit Report into a verified, risk-free response.</p>
        </div>
        """, unsafe_allow_html=True)


# 2. CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
             st.markdown(message["content"])
        else:
             st.write(message["content"])

# 3. CHAT INPUT
if prompt := st.chat_input("Enter your research query..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        
        status_container = st.status("🔍 Initializing Neural Search...", expanded=True)
        
        col_draft, col_audit = st.columns(2)
        draft_placeholder = col_draft.empty()
        audit_placeholder = col_audit.empty()
        final_placeholder = st.empty()
        
        full_response = ""
        
        try:
            # 600s Timeout for CPU safety
            with requests.post(f"{API_URL}/query_stream", json={"query": prompt}, stream=True, timeout=600) as r:
                if r.status_code != 200:
                     status_container.update(label="API Error", state="error")
                     st.error(f"Error {r.status_code}")
                else:
                    for line in r.iter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                
                                if data["type"] == "status":
                                    status_container.write(f"⚡ {data['content']}")
                                
                                elif data["type"] == "sources":
                                    source_list = [f"`{s}`" for s in data['content']]
                                    status_container.markdown(f"**📚 Reference Context:** {' '.join(source_list)}")
                                    
                                elif data["type"] == "draft":
                                    with draft_placeholder.container():
                                        st.info("**🧠 Synthesis (Draft)**")
                                        st.markdown(f"<div style='font-size: 0.85em; color: grey; max-height: 200px; overflow-y: auto;'>{data['content']}</div>", unsafe_allow_html=True)
                                    status_container.write("✅ Draft Generated")
                                    
                                elif data["type"] == "audit":
                                    with audit_placeholder.container():
                                        if "VERIFIED" in data["content"] or "Approved" in data["content"]:
                                            st.success("**🛡️ Compliance (Pass)**")
                                        else:
                                            st.warning("**🛡️ Compliance (Flag)**")
                                        st.markdown(f"<div style='font-size: 0.85em; max-height: 200px; overflow-y: auto;'>{data['content']}</div>", unsafe_allow_html=True)
                                    status_container.write("✅ Audit Complete")
                                    
                                elif data["type"] == "final":
                                    status_container.update(label="Analysis Complete", state="complete", expanded=False)
                                    final_placeholder.markdown(f"### 📋 Executive Intelligence Report\n\n{data['content']}")
                                    full_response = data['content']
                                    
                                elif data["type"] == "error":
                                     status_container.update(label="Error", state="error")
                                     st.error(data['content'])

                            except json.JSONDecodeError:
                                continue

            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.download_button("📥 Download Report", full_response, "report.txt")
                            
        except Exception as e:
            status_container.update(label="Error", state="error")
            st.error(f"Connection Error: {e}")
