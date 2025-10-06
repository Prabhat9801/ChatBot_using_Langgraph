import streamlit as st
from Langgraph_tool_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

# =========================== Page Configuration ===========================
st.set_page_config(
    page_title="LangGraph AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================== Custom CSS ===========================
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        color: white;
    }
    
    /* Chat message styling */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        background-color: transparent;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat input */
    .stChatInput {
        border-radius: 25px;
    }
    
    /* Title styling */
    h1 {
        color: white;
        text-align: center;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Sidebar titles */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* About section */
    .about-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .about-box h3 {
        color: #ffd700;
        margin-bottom: 10px;
    }
    
    .about-box p {
        color: white;
        line-height: 1.6;
    }
    
    /* Status indicator */
    .status-badge {
        background: #10b981;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
    }
    
    /* Thread buttons */
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 5px 0;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Markdown content in chat */
    .stMarkdown {
        color: #1f2937;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# =========================== Utilities ===========================
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

# ======================= Session Initialization ===================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "show_about" not in st.session_state:
    st.session_state["show_about"] = False

add_thread(st.session_state["thread_id"])

# ============================ Sidebar ============================
with st.sidebar:
    st.markdown("# 🤖 LangGraph AI")
    st.markdown("### Intelligent Chat Assistant")
    
    # Status badge
    st.markdown('<div class="status-badge">🟢 Online</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About button
    if st.button("ℹ️ About This App", use_container_width=True):
        st.session_state["show_about"] = not st.session_state["show_about"]
    
    # About section
    if st.session_state["show_about"]:
        with st.expander("📖 About LangGraph Chatbot", expanded=True):
            st.markdown("""
            ### 🚀 LangGraph AI Chatbot
            
            **Version:** 1.0.0  
            **Built by:** Prabhat Singh
            
            #### 🌟 Features:
            - 💬 **Conversational AI** powered by Google Gemini
            - 🔧 **Multi-Tool Support**:
              - 🧮 Calculator for math operations
              - 📈 Real-time stock price lookup
              - 🔍 Web search capabilities
            - 💾 **Persistent Conversations** with thread management
            - ⚡ **Real-time Streaming** responses
            - 🎯 **Context-Aware** interactions
            
            #### 🛠️ Tech Stack:
            - **LangGraph** - Stateful multi-agent framework
            - **Streamlit** - Interactive web interface
            - **Google Gemini 2.0** - Advanced AI model
            - **SQLite** - Conversation persistence
            
            #### 📧 Contact:
            For questions or feedback, reach out to Prabhat Singh
            
            ---
            *Made with ❤️ using LangGraph & Streamlit*
            """)
    
    st.markdown("---")
    
    # New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        reset_chat()
        st.rerun()
    
    st.markdown("### 📝 My Conversations")
    st.caption(f"Total: {len(st.session_state['chat_threads'])} threads")
    
    # Display threads with better formatting
    if st.session_state["chat_threads"]:
        for idx, thread_id in enumerate(st.session_state["chat_threads"][::-1], 1):
            thread_label = f"💬 Conversation {len(st.session_state['chat_threads']) - idx + 1}"
            if st.button(thread_label, key=str(thread_id), use_container_width=True):
                st.session_state["thread_id"] = thread_id
                messages = load_conversation(thread_id)
                
                temp_messages = []
                for msg in messages:
                    role = "user" if isinstance(msg, HumanMessage) else "assistant"
                    temp_messages.append({"role": role, "content": msg.content})
                st.session_state["message_history"] = temp_messages
                st.rerun()
    else:
        st.info("No conversations yet. Start chatting!")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8em;'>
        <p>Built by Prabhat Singh</p>
        <p>Powered by LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

# ============================ Main UI ============================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🤖 LangGraph AI Chatbot")
    st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Your Intelligent Assistant with Multi-Tool Capabilities</p>", unsafe_allow_html=True)

st.markdown("---")

# Chat container
chat_container = st.container()

with chat_container:
    # Render history with markdown support
    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])

# Chat input
user_input = st.chat_input("💭 Ask me anything...")

if user_input:
    # Show user's message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }

    # Assistant streaming block
    with st.chat_message("assistant", avatar="🤖"):
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    tool_emoji = {
                        "calculator": "🧮",
                        "get_stock_price": "📈",
                        "duckduckgo_search": "🔍"
                    }.get(tool_name, "🔧")
                    
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"{tool_emoji} Using `{tool_name}` ...", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"{tool_emoji} Using `{tool_name}` ...",
                            state="running",
                            expanded=True,
                        )

                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool execution completed", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
