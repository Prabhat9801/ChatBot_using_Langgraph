import sqlite3
import bcrypt
from datetime import datetime
import json

class Database:
    def __init__(self, db_name="chatbot_app.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                conversation_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, str(e)
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT user_id, password_hash FROM users WHERE username = ?',
            (username,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            user_id, password_hash = result
            if bcrypt.checkpw(password.encode('utf-8'), password_hash):
                return True, user_id
        
        return False, None
    
    def get_user_conversations(self, user_id):
        """Get all conversations for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            '''SELECT conversation_id, title, created_at, updated_at 
               FROM conversations 
               WHERE user_id = ? 
               ORDER BY updated_at DESC''',
            (user_id,)
        )
        
        conversations = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': conv[0],
                'title': conv[1],
                'created_at': conv[2],
                'updated_at': conv[3]
            }
            for conv in conversations
        ]
    
    def create_conversation(self, user_id, conversation_id, title="New Chat"):
        """Create a new conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO conversations (conversation_id, user_id, title) VALUES (?, ?, ?)',
            (conversation_id, user_id, title)
        )
        
        conn.commit()
        conn.close()
    
    def update_conversation_title(self, conversation_id, title):
        """Update conversation title"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE conversations SET title = ?, updated_at = ? WHERE conversation_id = ?',
            (title, datetime.now(), conversation_id)
        )
        
        conn.commit()
        conn.close()
    
    def update_conversation_timestamp(self, conversation_id):
        """Update conversation's last updated timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE conversations SET updated_at = ? WHERE conversation_id = ?',
            (datetime.now(), conversation_id)
        )
        
        conn.commit()
        conn.close()
    
    def delete_conversation(self, conversation_id):
        """Delete a conversation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM conversations WHERE conversation_id = ?', (conversation_id,))
        
        conn.commit()
        conn.close()
    
    def get_username(self, user_id):
        """Get username by user_id"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
