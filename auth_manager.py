import streamlit as st
from database import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
        
        # Initialize session state
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
        if 'username' not in st.session_state:
            st.session_state.username = None
    
    def login_page(self):
        """Display login/signup page"""
        st.markdown("""
        
            .auth-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 40px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            .auth-title {
                text-align: center;
                color: white;
                font-size: 2.5em;
                margin-bottom: 30px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
        
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('🤖 LangGraph AI', unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
            
            with tab1:
                self.login_form()
            
            with tab2:
                self.signup_form()
    
    def login_form(self):
        """Login form"""
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    success, user_id = self.db.authenticate_user(username, password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    def signup_form(self):
        """Signup form"""
        with st.form("signup_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Create a password")
            password_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if username and email and password and password_confirm:
                    if password == password_confirm:
                        if len(password) >= 6:
                            success, result = self.db.create_user(username, email, password)
                            if success:
                                st.success("✅ Account created successfully! Please login.")
                            else:
                                st.error(f"❌ {result}")
                        else:
                            st.warning("⚠️ Password must be at least 6 characters")
                    else:
                        st.error("❌ Passwords do not match")
                else:
                    st.warning("⚠️ Please fill in all fields")
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.clear()
        st.rerun()
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
