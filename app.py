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

# Enhanced Custom CSS - Replace the st.markdown CSS section with this

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Font */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* ==================== MAIN BACKGROUND ==================== */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
        min-height: 100vh;
        position: relative;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Animated background overlay */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
        pointer-events: none;
        z-index: 1;
    }
    
    .block-container {
        background: transparent !important;
        position: relative;
        z-index: 2;
        max-width: 1200px;
        padding: 2rem 1rem !important;
    }
    
    /* ==================== SIDEBAR ==================== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(45deg, transparent 30%, rgba(102, 126, 234, 0.05) 50%, transparent 70%);
        animation: sidebarShine 3s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes sidebarShine {
        0%, 100% { opacity: 0; }
        50% { opacity: 1; }
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        animation: slideInSmooth 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideInSmooth {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Sidebar text colors */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* ==================== CHAT MESSAGES ==================== */
    .stChatMessage {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.98) 100%) !important;
        border-radius: 20px;
        padding: 24px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: messageSlideIn 0.5s ease-out;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Chat message text */
    .stChatMessage p, 
    .stChatMessage span,
    .stChatMessage div {
        color: #1a1a2e !important;
        line-height: 1.6;
    }
    
    /* Chat avatars */
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
    }
    
    /* ==================== BUTTONS ==================== */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
        padding: 0.65rem 1.2rem;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #5568d3 0%, #6a3d8f 100%) !important;
    }
    
    .stButton>button:active {
        transform: translateY(-1px);
    }
    
    /* ==================== HEADERS ==================== */
    .main h1 {
        color: white !important;
        font-weight: 800 !important;
        text-align: center;
        font-size: 3rem !important;
        letter-spacing: -0.5px;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.5rem !important;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .main h2, .main h3 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
    }
    
    /* All main content text - but NOT inputs, labels, or form elements */
    .main > div > div > div > h1,
    .main > div > div > div > h2,
    .main > div > div > div > h3 {
        color: white !important;
        font-weight: 500;
    }
    
    /* Subtitle styling - only for chatbot page */
    .main > div > div > div:first-child p[style*="text-align: center"] {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 600 !important;
        font-size: 1.15em !important;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        animation: fadeIn 1s ease-out 0.3s both;
        display: none !important; /* Hide subtitle */
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* ==================== USER INFO CARD ==================== */
    .user-info {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.1) 100%) !important;
        padding: 20px;
        border-radius: 16px;
        margin: 15px 0;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .user-info:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.15) 100%) !important;
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .user-info h4, .user-info p {
        color: white !important;
    }
    
    /* ==================== SIDEBAR BUTTONS ==================== */
    [data-testid="stSidebar"] .stButton>button {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.1) 100%) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.2) 100%) !important;
        transform: translateX(5px);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* ==================== TOOL INDICATOR ==================== */
    .tool-indicator {
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 14px 28px;
        border-radius: 50px;
        font-size: 1.05em;
        font-weight: 700;
        margin: 15px 0;
        box-shadow: 0 8px 30px rgba(245, 87, 108, 0.4);
        animation: toolPulse 2s ease-in-out infinite;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes toolPulse {
        0%, 100% {
            transform: scale(1);
            box-shadow: 0 8px 30px rgba(245, 87, 108, 0.4);
        }
        50% {
            transform: scale(1.05);
            box-shadow: 0 12px 40px rgba(245, 87, 108, 0.6);
        }
    }
    
    /* ==================== STATUS CONTAINER ==================== */
    .stStatus {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
        border-radius: 16px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        color: #1a1a2e !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .stStatus * {
        color: #1a1a2e !important;
    }
    
    /* ==================== INFO & SUCCESS BOXES ==================== */
    .info-box {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.3) 0%, rgba(0, 242, 254, 0.2) 100%) !important;
        border-left: 5px solid #4facfe;
        padding: 18px 20px;
        border-radius: 12px;
        margin: 15px 0;
        color: white !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2);
        font-weight: 500;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.3) 0%, rgba(16, 185, 129, 0.2) 100%) !important;
        border-left: 5px solid #22c55e;
        padding: 18px 20px;
        border-radius: 12px;
        margin: 15px 0;
        color: white !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.2);
        font-weight: 500;
        animation: successSlide 0.5s ease-out;
    }
    
    @keyframes successSlide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* ==================== CHAT INPUT ==================== */
    .stChatInputContainer {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%) !important;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(20px);
    }
    
    .stChatInput textarea {
        background: white !important;
        color: #1a1a2e !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
    }
    
    .stChatInput textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        outline: none !important;
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2) 0%, rgba(255, 255, 255, 0.15) 100%) !important;
        color: white !important;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.2) 100%) !important;
        transform: translateX(5px);
    }
    
    .streamlit-expanderContent {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0.1) 100%) !important;
        border-radius: 0 0 12px 12px;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: none;
        backdrop-filter: blur(10px);
    }
    
    /* ==================== SCROLLBAR ==================== */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.6) 0%, rgba(118, 75, 162, 0.6) 100%);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
    }
    
    /* ==================== DIVIDER ==================== */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* ==================== CAPTIONS ==================== */
    .stCaption {
        color: rgba(255, 255, 255, 0.85) !important;
        font-weight: 500;
    }
    
    /* ==================== HIDE SPECIFIC ELEMENTS ==================== */
    /* Only hide the menu hint in the header area */
    .main > div > div > div:first-child [data-testid="column"]:last-child {
        display: none !important;
    }
    
    /* ==================== RESPONSIVE DESIGN ==================== */
    @media (max-width: 768px) {
        .main h1 {
            font-size: 2rem !important;
        }
        
        .tool-indicator {
            font-size: 0.9em;
            padding: 10px 18px;
        }
        
        .stChatMessage {
            padding: 18px;
            margin: 15px 0;
        }
        
        .block-container {
            padding: 1rem 0.5rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .main h1 {
            font-size: 1.5rem !important;
        }
        
        .user-info {
            padding: 15px;
        }
        
        .stButton>button {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
        
        .tool-indicator {
            font-size: 0.85em;
            padding: 8px 14px;
        }
    }
    
    /* ==================== LOADING ANIMATIONS ==================== */
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    /* ==================== HOVER EFFECTS ==================== */
    .stChatMessage:hover::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(102, 126, 234, 0.05), transparent);
        pointer-events: none;
        border-radius: 20px;
    }
    
    /* ==================== FINAL OVERRIDES ==================== */
    /* Only force white color on headers in main area */
    .main h1,
    .main h2,
    .main h3 {
        color: white !important;
    }
    
    /* Keep chat messages, status, and inputs dark */
    .stChatMessage *,
    .stStatus *,
    .stChatInput *,
    .stTextInput *,
    input,
    textarea,
    label,
    .stButton button span {
        color: #1a1a2e !important;
    }
    
    /* Make sure form elements are visible */
    .stTextInput input {
        color: #1a1a2e !important;
        background: white !important;
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
#     st.markdown("<p style='text-align: center; color: white; font-size: 1.1em;'>Your Intelligent Multi-Tool Assistant</p>", unsafe_allow_html=True)
# with col2:
#     st.markdown('<div style="text-align: right; color: white; font-size: 0.9em; padding-top: 20px;">👈 Open menu for conversations</div>', unsafe_allow_html=True)

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
