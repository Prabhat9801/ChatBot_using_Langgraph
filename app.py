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
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    h1, h2, h3 {
        color: white !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p {
        color: white !important;
    }
    
    .user-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    
    [data-testid="stSidebar"] .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255, 255, 255, 0.2);
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

init_session_state()

# Utilities
def reset_chat():
    thread_id = str(uuid.uuid4())
    st.session_state.thread_id = thread_id
    st.session_state.message_history = []
    db.create_conversation(st.session_state.user_id, thread_id, "New Chat")
    st.session_state.conversations = db.get_user_conversations(st.session_state.user_id)

def load_conversation(conversation_id):
    st.session_state.thread_id = conversation_id
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

# Sidebar
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
            - 🔐 Secure Authentication
            - 💬 Persistent Conversations
            - 🛠️ 6 Powerful Tools:
              - 🧮 Advanced Calculator
              - 🔍 Web Search
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
                if st.button(
                    f"💭 {conv['title'][:30]}",
                    key=f"load_{conv['id']}",
                    use_container_width=True
                ):
                    load_conversation(conv['id'])
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"del_{conv['id']}"):
                    delete_conversation(conv['id'])
                    st.rerun()
    else:
        st.info("No conversations yet")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8em;'>
        <p>© 2025 Prabhat Singh</p>
        <p>Powered by LangGraph</p>
    </div>
    """, unsafe_allow_html=True)

# Main UI
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("# 🤖 LangGraph AI Chatbot")
    st.markdown("<p style='text-align: center; color: white;'>Your Intelligent Multi-Tool Assistant</p>", unsafe_allow_html=True)

st.markdown("---")

# Chat history
for message in st.session_state.message_history:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("💭 Ask me anything...")

if user_input:
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
        
        def ai_stream():
            for message_chunk, metadata in st.session_state.chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    tool_emojis = {
                        "calculator": "🧮",
                        "web_search": "🔍",
                        "get_stock_price": "📈",
                        "wikipedia_search": "📚",
                        "news_search": "📰",
                        "currency_converter": "💱"
                    }
                    emoji = tool_emojis.get(tool_name, "🔧")
                    
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"{emoji} Using {tool_name}...",
                            expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"{emoji} Using {tool_name}...",
                            state="running",
                            expanded=True
                        )
                
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content
        
        ai_message = st.write_stream(ai_stream())
        
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Complete",
                state="complete",
                expanded=False
            )
    
    st.session_state.message_history.append(
        {"role": "assistant", "content": ai_message}
    )
