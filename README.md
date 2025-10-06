```markdown
# LangGraph Chatbot

A conversational AI chatbot built with LangGraph, Streamlit, and Google Gemini.

## Features
- Multi-tool support (Calculator, Stock prices, Web search)
- Conversation history with thread management
- Persistent storage with SQLite
- Real-time streaming responses

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your `GOOGLE_API_KEY`
4. Run: `streamlit run app.py`

## Deployment
See deployment guide for instructions on deploying to Streamlit Cloud, Render, or Railway.
```

---

## 🚀 Local Installation & Running

### Step 1: Create Project Directory
```bash
mkdir langgraph-chatbot
cd langgraph-chatbot
```

### Step 2: Create All Files
Create all the files listed above with their respective content.

### Step 3: Install Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 4: Configure Environment
1. Get a Google API key from: https://makersuite.google.com/app/apikey
2. Create `.env` file and add:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Step 5: Run Locally
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Deployment Options

## Option 1: Streamlit Cloud (FREE & EASIEST)

### Steps:
1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/langgraph-chatbot.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub repository
   - Select the repository and branch
   - Set main file path: `app.py`
   - Click "Advanced settings" → Add secrets:
     ```
     GOOGLE_API_KEY = "your_api_key_here"
     ```
   - Click "Deploy"

3. **Your app will be live at**: `https://yourusername-langgraph-chatbot.streamlit.app`

---

## Option 2: Render (FREE)

### Steps:
1. **Push to GitHub** (same as above)

2. **Deploy on Render**
   - Go to https://render.com/
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: langgraph-chatbot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Add Environment Variable:
     - Key: `GOOGLE_API_KEY`
     - Value: your_api_key
   - Click "Create Web Service"

3. **Your app will be live at**: `https://langgraph-chatbot.onrender.com`

---

## Option 3: Railway (FREE)

### Steps:
1. **Push to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to https://railway.app/
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect it's a Python app
   - Add Environment Variable:
     - Key: `GOOGLE_API_KEY`
     - Value: your_api_key
   - Click "Deploy"

3. **Your app will be live at**: Railway will provide a URL

---

## Option 4: Hugging Face Spaces (FREE)

### Steps:
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose "Streamlit" as SDK
4. Upload all your files
5. Add your `GOOGLE_API_KEY` in Settings → Repository secrets
6. Your app will be live!

---

## 🔧 Troubleshooting

### Common Issues:

1. **"No module named 'streamlit'"**
   - Solution: `pip install -r requirements.txt`

2. **"GOOGLE_API_KEY not found"**
   - Solution: Create `.env` file with your API key

3. **Database locked error**
   - Solution: Delete `chatbot.db` and restart

4. **Port already in use**
   - Solution: `streamlit run app.py --server.port=8502`

---

## 📊 Testing Your Deployment

After deployment, test these features:
1. ✅ Send a message
2. ✅ Ask for a calculation: "What is 25 * 4?"
3. ✅ Ask for stock price: "What's the price of AAPL?"
4. ✅ Ask to search web: "Latest news about AI"
5. ✅ Create a new chat
6. ✅ Switch between conversations

---

## 🎉 Success!

Your chatbot is now deployed and accessible worldwide! Share the URL with anyone.

**Need help?** Check the respective platform's documentation:
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Render: https://render.com/docs
- Railway: https://docs.railway.app/

Happy chatting! 🚀
```
