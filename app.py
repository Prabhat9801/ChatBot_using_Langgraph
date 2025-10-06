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
    }
</style>
""", unsafe_allow_html=True)
