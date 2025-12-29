import streamlit as st
import requests

# 1. Page settings
st.set_page_config(
    page_title="Drug Discovery AI | Medical Agent",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. UI enhancements (without changing the input box size)
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    
    /* Improve chat bubble appearance only */
    .stChatMessage { 
        padding: 1rem; 
        border-radius: 12px; 
        margin-bottom: 0.5rem; 
        border: 1px solid #f0f0f0;
    }
    
    /* Very minimal customization for the input box to keep it clean */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/822/822143.png", width=80)
    st.title("Dashboard")
    st.markdown("---")
    
    st.subheader("🌐 System Status")
    st.success("● Browser connected")
    st.info("● Llama 3.3 engine ready")
    
    st.markdown("---")
    st.subheader("📚 Activated Sources")
    st.write("✓ Neo4j Graph Database")
    st.write("✓ PubMed Central")
    st.write("✓ Tavily Web Search")
    
    # Clear memory button
    if st.button("🗑️ New Chat", help="Clear conversation history"):
        st.session_state.messages = []
        st.rerun()

# 5. Main title
st.title("🧬 Drug Discovery RAG Explorer")
st.caption("AI-powered expert system for drug interactions and clinical research.")
st.markdown("---")

# 6. Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        else:
            # Extract stored data
            data = message["content"]
            
            # Display the answer
            st.markdown("### 🤖 Scientific Analysis")
            st.info(data.get("answer", "No answer available."))
            
            # Display sources
            sources = data.get("sources", {})
            tab_graph, tab_pubmed, tab_web = st.tabs(["🧬 Graph", "📖 PubMed", "🌐 Web"])
            
            with tab_graph:
                st.code(sources.get("graph", "No data."), language="text")
            with tab_pubmed:
                st.markdown(f"> {sources.get('local_literature', 'No data.')}")
            with tab_web:
                st.write(sources.get("web_updates", "No data."))

# 7. Input box
if prompt := st.chat_input("Ask a medical question (e.g., Aspirin side effects)..."):
    
    # A. Display and store the user's question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # B. Process the bot response
    with st.chat_message("assistant"):
        with st.status("🔍 Analyzing clinical data...", expanded=True) as status:
            try:
                # Call the API
                response = requests.post("http://127.0.0.1:8000/ask", json={"prompt": prompt}, timeout=100)
                
                if response.status_code == 200:
                    data = response.json()
                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    
                    # Display results
                    st.markdown("### 🤖 Scientific Analysis")
                    st.info(data.get("answer"))
                    
                    sources = data.get("sources", {})
                    tab_graph, tab_pubmed, tab_web = st.tabs(["🧬 Graph", "📖 PubMed", "🌐 Web"])
                    
                    with tab_graph:
                        st.code(sources.get("graph", "No data."), language="text")
                    with tab_pubmed:
                        st.markdown(f"> {sources.get('local_literature', 'No data.')}")
                    with tab_web:
                        st.write(sources.get("web_updates", "No data."))
                    
                    # Store the bot response in memory
                    st.session_state.messages.append({"role": "assistant", "content": data})
                    
                else:
                    status.update(label="❌ Server Error", state="error")
                    st.error(f"Error: {response.status_code}")
                    
            except Exception as e:
                status.update(label="⚠️ Connection Failed", state="error")
                st.error(f"Error: {str(e)}")
