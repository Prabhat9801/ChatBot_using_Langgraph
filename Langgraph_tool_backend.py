from langgraph.graph import StateGraph, START
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests
import os
from duckduckgo_search import DDGS
import wikipedia

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform arithmetic operations on two numbers.
    Operations: add, sub, mul, div, pow, mod
    """
    try:
        operations = {
            "add": lambda a, b: a + b,
            "sub": lambda a, b: a - b,
            "mul": lambda a, b: a * b,
            "div": lambda a, b: a / b if b != 0 else None,
            "pow": lambda a, b: a ** b,
            "mod": lambda a, b: a % b if b != 0 else None
        }
        
        if operation not in operations:
            return {"error": f"Unsupported operation: {operation}"}
        
        result = operations[operation](first_num, second_num)
        
        if result is None:
            return {"error": "Division by zero"}
        
        return {
            "first_num": first_num,
            "second_num": second_num,
            "operation": operation,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}

@tool
def web_search(query: str, max_results: int = 5) -> dict:
    """
    Search the web using DuckDuckGo for current information and news.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        
        formatted_results = []
        for r in results:
            formatted_results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        
        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results)
        }
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a symbol like AAPL, TSLA, GOOGL.
    """
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "IKL4A9NNABD44FKE")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            return {
                "symbol": symbol,
                "price": quote.get("05. price", "N/A"),
                "change": quote.get("09. change", "N/A"),
                "change_percent": quote.get("10. change percent", "N/A"),
                "volume": quote.get("06. volume", "N/A")
            }
        else:
            return {"error": "Stock data not found"}
    except Exception as e:
        return {"error": f"Failed: {str(e)}"}

@tool
def wikipedia_search(query: str) -> dict:
    """
    Search Wikipedia for factual information and summaries.
    """
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
        page = wikipedia.page(query, auto_suggest=True)
        
        return {
            "title": page.title,
            "summary": summary,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        return {
            "error": "Multiple results found",
            "suggestions": e.options[:5]
        }
    except wikipedia.exceptions.PageError:
        return {"error": f"No page found for: {query}"}
    except Exception as e:
        return {"error": f"Failed: {str(e)}"}

@tool
def news_search(topic: str, max_results: int = 5) -> dict:
    """
    Get latest news articles about a topic using DuckDuckGo News.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.news(topic, max_results=max_results))
        
        articles = []
        for article in results:
            articles.append({
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "source": article.get("source", ""),
                "date": article.get("date", ""),
                "snippet": article.get("body", "")
            })
        
        return {
            "topic": topic,
            "articles": articles,
            "count": len(articles)
        }
    except Exception as e:
        return {"error": f"News search failed: {str(e)}"}

@tool
def currency_converter(amount: float, from_currency: str, to_currency: str) -> dict:
    """
    Convert currency using live exchange rates.
    Example: amount=100, from_currency=USD, to_currency=EUR
    """
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "rates" in data:
            to_curr = to_currency.upper()
            if to_curr in data["rates"]:
                rate = data["rates"][to_curr]
                converted = amount * rate
                return {
                    "from": from_currency.upper(),
                    "to": to_currency.upper(),
                    "amount": amount,
                    "converted_amount": round(converted, 2),
                    "exchange_rate": rate
                }
            else:
                return {"error": f"Currency not found: {to_currency}"}
        else:
            return {"error": "Failed to fetch rates"}
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}

tools = [
    calculator,
    web_search,
    get_stock_price,
    wikipedia_search,
    news_search,
    currency_converter
]

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    
    if not response.content or "I cannot" in response.content:
        response = llm.invoke(messages)
    
    return {"messages": [response]}

tool_node = ToolNode(tools)

def get_user_checkpointer(user_id):
    db_path = f"user_{user_id}_chats.db"
    conn = sqlite3.connect(database=db_path, check_same_thread=False)
    return SqliteSaver(conn=conn)

def create_chatbot(user_id):
    checkpointer = get_user_checkpointer(user_id)
    
    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)
    
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge('tools', 'chat_node')
    
    return graph.compile(checkpointer=checkpointer)

def retrieve_user_threads(user_id):
    checkpointer = get_user_checkpointer(user_id)
    all_threads = set()
    
    try:
        for checkpoint in checkpointer.list(None):
            thread_id = checkpoint.config["configurable"]["thread_id"]
            all_threads.add(thread_id)
    except:
        pass
    
    return list(all_threads)

def generate_conversation_title(first_message: str) -> str:
    """Generate a short title from the first message"""
    title = first_message[:50]
    if len(first_message) > 50:
        title += "..."
    return title
