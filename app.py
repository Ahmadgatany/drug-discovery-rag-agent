import streamlit as st
import requests

# 1. Page settings
st.set_page_config(
    page_title="Drug Discovery AI | Medical Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. UI enhancements with RTL support and icon rendering fixes
st.markdown("""
    <style>
    /* Import fonts and libraries */
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    /* Apply Arabic font */
    html, body, [class*="st-"] {
        font-family: 'Tajawal', sans-serif;
    }

    .stApp { background-color: #fcfcfc; }
    
    /* Right-to-left text alignment */
    .rtl-text {
        direction: rtl;
        text-align: right;
        line-height: 1.8;
    }
    
    /* Chat bubble styling */
    .stChatMessage { 
        padding: 1.2rem; 
        border-radius: 15px; 
        margin-bottom: 1rem; 
        border: 1px solid #eef0f2;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }

    /* Scientific analysis container */
    .analysis-box {
        background-color: #f0f7ff;
        border-right: 5px solid #007bff;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        font-size: 1.1rem;
        color: #1a1a1a;
    }

    .analysis-box b, .analysis-box strong {
        color: #0056b3;
    }

    /* Fix icon label rendering issues */
    .material-icons {
        font-family: 'Material Icons' !important;
    }
    
    /* Hide any broken icon text labels */
    span[data-testid="stSidebarCollapseIcon"] {
        font-family: 'Material Icons' !important;
    }
    </style>
    """, unsafe_allow_html=True)

USER_AVATAR = "👤"
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/3858/3858711.png"

# 3. Assistant response rendering function
def display_assistant_response(data, msg_index):
    """
    Render the assistant response with text cleaning and RTL handling
    """
    answer = data.get("answer", "No answer available.")
    sources = data.get("sources", {})
    
    st.markdown("### 🤖 Scientific Analysis")
    
    # Clean technical icon-related tokens that may appear in text
    clean_answer = answer.replace("keyboard_double_arrow_right", "»")
    clean_answer = clean_answer.replace("keyboard_double_arrow_left", "«")
    clean_answer = clean_answer.replace("keyboard_double_arrow_down", "▼")
    
    # Improve bullet point formatting for Arabic readability
    formatted_answer = clean_answer.replace("\n- ", "\n» ").replace("\n* ", "\n» ")
    
    # Render text inside an RTL container with enhanced styling
    st.markdown(
        f'<div class="rtl-text analysis-box">{formatted_answer}</div>',
        unsafe_allow_html=True
    )
    
    # Report download button
    st.download_button(
        label="📥 Download Analysis Report",
        data=answer,
        file_name=f"medical_report_{msg_index}.md",
        mime="text/markdown",
        key=f"btn_dl_{msg_index}"
    )
    
    # Source tabs
    tab_graph, tab_pubmed, tab_web = st.tabs([
        "🧬 Knowledge Graph",
        "📖 PubMed Literature",
        "🌐 Real-time Web"
    ])
    
    with tab_graph:
        st.info("⚡ Structured Data Nodes (Neo4j)")
        st.code(sources.get("graph", "No structured data found."), language="text")
    
    with tab_pubmed:
        st.caption("Evidence-based literature snippets:")
        st.markdown(
            f'<div class="rtl-text" style="background:#f9f9f9; padding:10px; border-radius:5px;">'
            f'{sources.get("local_literature", "No literature found.")}'
            f'</div>',
            unsafe_allow_html=True
        )
        
    with tab_web:
        st.caption("Latest updates from search engines (2025):")
        st.write(sources.get("web_updates", "No data available."))

# 4. Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80)
    st.title("Medical Explorer")
    st.markdown("---")
    
    st.subheader("🌐 System Status")
    st.markdown("🟢 **Engine:** Llama 3.3 (Graph-RAG)")
    st.markdown("📅 **Knowledge Cutoff:** Dec 2025")
    
    st.markdown("---")
    st.subheader("📚 Activated Sources")
    st.markdown("🔵 `Neo4j` Graph Database")
    st.markdown("🟢 `PubMed` Central (API)")
    st.markdown("🟣 `Tavily` Search Engine")
    
    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Main interface
st.title("🧬 Drug Discovery RAG Explorer")
st.caption("Expert AI Agent for Clinical Mechanism Analysis & Drug Interactions")
st.markdown("---")

# 7. Display conversation history
for idx, message in enumerate(st.session_state.messages):
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        if message["role"] == "user":
            st.markdown(
                f'<div class="rtl-text">{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            display_assistant_response(message["content"], idx)

# 8. User input
if prompt := st.chat_input("Ask about drugs, genes, or pathways..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(f'<div class="rtl-text">{prompt}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.status("🔍 Orchestrating Multi-Source Search...", expanded=True) as status:
            try:
                # Send request to the backend
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json={"prompt": prompt},
                    timeout=150
                )
                
                if response.status_code == 200:
                    data = response.json()
                    status.update(
                        label="✅ Analysis Complete!",
                        state="complete",
                        expanded=False
                    )
                    st.toast("Scientific report generated!", icon="⚡")
                    
                    current_idx = len(st.session_state.messages)
                    display_assistant_response(data, current_idx)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data
                    })
                else:
                    status.update(label="❌ API Error", state="error")
                    st.error(f"Backend error: {response.status_code}")
                    
            except Exception as e:
                status.update(label="⚠️ Critical Error", state="error")
                st.error(f"Connection failed: {str(e)}")
