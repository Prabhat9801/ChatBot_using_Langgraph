import streamlit as st
from Langgraph_tool_backend import create_chatbot, retrieve_user_threads, generate_conversation_title
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from auth_manager import AuthManager
from database import Database
import uuid

# Page config
st.set_page_config(
    page_title="LangGraph AI - Multi-Tool Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with better light/dark mode support
st.markdown("""
<style>
    /* Main gradient background - works in both modes */
    .main {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
        min-height: 100vh;
    }
    
    /* Ensure main content area has proper styling */
    .block-container {
        background: transparent !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        box-shadow: 2px 0 10px rgba(0,0,0,0.3);
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
        }
        to {
            transform: translateX(0);
        }
    }
    
    /* Force sidebar text to be white */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Chat message styling - improved contrast */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
    }
    
    /* Force chat message text to be dark for readability */
    .stChatMessage p, 
    .stChatMessage span,
    .stChatMessage div {
        color: #1e293b !important;
    }
    
    /* Avatar styling */
    .stChatMessage [data-testid="chatAvatarIcon-user"],
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none;
        padding: 0.5rem 1rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    }
    
    /* Main headers - high contrast white with shadow */
    .main h1, .main h2, .main h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        font-weight: 700 !important;
    }
    
    /* Main content text */
    .main p, .main span, .main div {
        color: white !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    /* User info card */
    .user-info {
        background: rgba(255, 255, 255, 0.15) !important;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .user-info h4, .user-info p {
        color: white !important;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        transform: translateX(5px);
    }
    
    /* Tool indicator badge */
    .tool-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 1em;
        font-weight: 600;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
            transform: scale(1);
        }
        50% {
            opacity: 0.9;
            transform: scale(1.02);
        }
    }
    
    /* Status container */
    .stStatus {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 10px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #1e293b !important;
    }
    
    .stStatus * {
        color: #1e293b !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Info box */
    .info-box {
        background: rgba(59, 130, 246, 0.25) !important;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    /* Success box */
    .success-box {
        background: rgba(34, 197, 94, 0.25) !important;
        border-left: 4px solid #22c55e;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: white !important;
        backdrop-filter: blur(10px);
    }
    
    /* Chat input styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .stChatInput textarea {
        background: white !important;
        color: #1e293b !important;
        border: 2px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stChatInput textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 0 0 8px 8px;
        color: white !important;
    }
    
    /* Caption styling */
    .stCaption {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Ensure all markdown in main area is white */
    .main .stMarkdown {
        color: white !important;
    }
    
    /* Column text */
    [data-testid="column"] {
        color: white !important;
    }
    
    [data-testid="column"] p,
    [data-testid="column"] div,
    [data-testid="column"] span {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        font-weight: 500;
    }
    
    /* Force inline styles to be white with shadow */
    [style*="color: white"] {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Specific fix for subtitle and menu hint */
    .main p[style*="text-align: center"],
    .main div[style*="text-align: right"] {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        font-weight: 600 !important;
    }
    
    /* Make sure all text in main area is visible */
    .main * {
        color: white !important;
    }
    
    /* But keep chat messages dark for readability */
    .stChatMessage * {
        color: #1e293b !important;
        text-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
auth_manager = AuthManager()
db = Database()

# Authentication check
if not auth_manager.is_authenticated():
    auth_manager.login_page()
    st.stop()

# Session state initialization
def init_session_state():
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = create_chatbot(st.session_state.user_id)
    
    if "message_history" not in st.session_state:
        st.session_state.message_history = []
    
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())
        db.create_conversation(
            st.session_state.user_id,
            st.session_state.thread_id,
            "New Chat"
        )
    
    if "conversations" not in st.session_state:
        st.session_state.conversations = db.get_user_conversations(st.session_state.user_id)
    
    if "show_about" not in st.session_state:
        st.session_state.show_about = False
    
    if "current_tool" not in st.session_state:
        st.session_state.current_tool = None

init_session_state()

# Utilities
def reset_chat():
    thread_id = str(uuid.uuid4())
    st.session_state.thread_id = thread_id
    st.session_state.message_history = []
    st.session_state.current_tool = None
    db.create_conversation(st.session_state.user_id, thread_id, "New Chat")
    st.session_state.conversations = db.get_user_conversations(st.session_state.user_id)

def load_conversation(conversation_id):
    st.session_state.thread_id = conversation_id
    st.session_state.current_tool = None
    state = st.session_state.chatbot.get_state(
        config={"configurable": {"thread_id": conversation_id}}
    )
    messages = state.values.get("messages", [])
    
    temp_messages = []
    for msg in messages:
        if isinstance(msg, (HumanMessage, AIMessage)):
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            temp_messages.append({"role": role, "content": msg.content})
    
    st.session_state.message_history = temp_messages

def delete_conversation(conversation_id):
    db.delete_conversation(conversation_id)
    if st.session_state.thread_id == conversation_id:
        reset_chat()
    st.session_state.conversations = db.get_user_conversations(st.session_state.user_id)

# Sidebar with slide animation
with st.sidebar:
    st.markdown("# 🤖 LangGraph AI")
    st.markdown("### Multi-Tool Assistant")
    
    st.markdown(f"""
    <div class="user-info">
        <h4>👤 {st.session_state.username}</h4>
        <p style="font-size: 0.9em; opacity: 0.8;">User ID: {st.session_state.user_id}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            auth_manager.logout()
    with col2:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state.show_about = not st.session_state.show_about
    
    if st.session_state.show_about:
        with st.expander("📖 About", expanded=True):
            st.markdown("""
            ### 🚀 LangGraph AI Chatbot
            
            **Version:** 2.0.0  
            **Developer:** Prabhat Singh
            
            #### 🌟 Features:
            - 🔐 **Secure Authentication**
            - 💬 **Persistent Conversations**
            - 🛠️ **6 Powerful Tools**:
              - 🧮 Advanced Calculator
              - 🔍 Web Search (DuckDuckGo)
              - 📈 Stock Price Tracker
              - 📚 Wikipedia Search
              - 📰 News Search
              - 💱 Currency Converter
            
            #### 🛠️ Tech Stack:
            - LangGraph + Google Gemini 2.0
            - Streamlit + SQLite
            - Authentication & Multi-user
            
            ---
            *Built with ❤️ by Prabhat Singh*
            """)
    
    st.markdown("---")
    
    if st.button("➕ New Chat", use_container_width=True):
        reset_chat()
        st.rerun()
    
    st.markdown("### 💬 My Conversations")
    st.caption(f"Total: {len(st.session_state.conversations)}")
    
    if st.session_state.conversations:
        for conv in st.session_state.conversations:
            col1, col2 = st.columns([4, 1])
            
            with col1:
                # Add conversation-btn class for hover effect
                button_key = f"load_{conv['id']}"
                if st.button(
                    f"💭 {conv['title'][:30]}",
                    key=button_key,
                    use_container_width=True
                ):
                    load_conversation(conv['id'])
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv['id']}", help="Delete conversation"):
                    delete_conversation(conv['id'])
                    st.rerun()
    else:
        st.markdown('<div class="info-box">📝 No conversations yet. Start chatting!</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8em;'>
        <p>© 2025 Prabhat Singh</p>
        <p>Powered by LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

# Main UI - Header with menu hint
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("# 🤖 LangGraph AI Chatbot")
    st.markdown("<p style='text-align: center; color: white; font-size: 1.1em;'>Your Intelligent Multi-Tool Assistant</p>", unsafe_allow_html=True)
with col2:
    st.markdown('<div style="text-align: right; color: white; font-size: 0.9em; padding-top: 20px;">👈 Open menu for conversations</div>', unsafe_allow_html=True)

st.markdown("---")

# Show current tool indicator if active
if st.session_state.current_tool:
    tool_emojis = {
        "calculator": "🧮",
        "web_search": "🔍",
        "get_stock_price": "📈",
        "wikipedia_search": "📚",
        "news_search": "📰",
        "currency_converter": "💱"
    }
    tool_names = {
        "calculator": "Calculator",
        "web_search": "Web Search",
        "get_stock_price": "Stock Price",
        "wikipedia_search": "Wikipedia",
        "news_search": "News Search",
        "currency_converter": "Currency Converter"
    }
    emoji = tool_emojis.get(st.session_state.current_tool, "🔧")
    name = tool_names.get(st.session_state.current_tool, st.session_state.current_tool)
    
    st.markdown(f"""
    <div class="tool-indicator">
        <span>{emoji}</span>
        <span>Using: {name}</span>
        <span>⚡</span>
    </div>
    """, unsafe_allow_html=True)

# Chat history
for message in st.session_state.message_history:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("💭 Ask me anything...")

if user_input:
    # Reset current tool
    st.session_state.current_tool = None
    
    # Update title if first message
    if len(st.session_state.message_history) == 0:
        title = generate_conversation_title(user_input)
        db.update_conversation_title(st.session_state.thread_id, title)
        st.session_state.conversations = db.get_user_conversations(st.session_state.user_id)
    
    db.update_conversation_timestamp(st.session_state.thread_id)
    
    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    CONFIG = {
        "configurable": {"thread_id": st.session_state.thread_id},
        "metadata": {"thread_id": st.session_state.thread_id},
        "run_name": "chat_turn",
    }
    
    with st.chat_message("assistant", avatar="🤖"):
        status_holder = {"box": None}
        tool_used = {"name": None}
        
        def ai_stream():
            for message_chunk, metadata in st.session_state.chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    tool_used["name"] = tool_name
                    st.session_state.current_tool = tool_name
                    
                    tool_emojis = {
                        "calculator": "🧮",
                        "web_search": "🔍",
                        "get_stock_price": "📈",
                        "wikipedia_search": "📚",
                        "news_search": "📰",
                        "currency_converter": "💱"
                    }
                    
                    tool_display_names = {
                        "calculator": "Calculator",
                        "web_search": "Web Search",
                        "get_stock_price": "Stock Price Lookup",
                        "wikipedia_search": "Wikipedia Search",
                        "news_search": "News Search",
                        "currency_converter": "Currency Converter"
                    }
                    
                    emoji = tool_emojis.get(tool_name, "🔧")
                    display_name = tool_display_names.get(tool_name, tool_name)
                    
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"{emoji} Using {display_name}...",
                            expanded=True,
                            state="running"
                        )
                        with status_holder["box"]:
                            st.write(f"🔄 Processing with **{display_name}**")
                    else:
                        status_holder["box"].update(
                            label=f"{emoji} Using {display_name}...",
                            state="running",
                            expanded=True
                        )
                
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content
        
        ai_message = st.write_stream(ai_stream())
        
        # Show completion status
        if status_holder["box"] is not None:
            tool_name = tool_used["name"]
            tool_emojis = {
                "calculator": "🧮",
                "web_search": "🔍",
                "get_stock_price": "📈",
                "wikipedia_search": "📚",
                "news_search": "📰",
                "currency_converter": "💱"
            }
            emoji = tool_emojis.get(tool_name, "🔧")
            
            status_holder["box"].update(
                label=f"✅ {emoji} Completed",
                state="complete",
                expanded=False
            )
            
            # Show success message
            st.markdown(f'<div class="success-box">✅ Successfully used {tool_name}</div>', unsafe_allow_html=True)
    
    # Save assistant message
    st.session_state.message_history.append(
        {"role": "assistant", "content": ai_message}
    )
    
    # Clear current tool after response
    st.session_state.current_tool = None
