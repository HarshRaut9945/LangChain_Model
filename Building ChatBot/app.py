from flask import Flask, render_template, request, redirect, url_for
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os, sqlite3,datetime

app = Flask(__name__)

# Configuration (LLMs, API, Prompt)
load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash',google_api_key=os.getenv('GOOGLE_API_KEY'))

DB_FILE="chatbot.db"

#db setup

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c=conn.curson()

    c.execute('''CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    created_at TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    sender TEXT,
                    text TEXT,
                    created_at TEXT,
                    FOREIGN KEY(chat_id) REFERENCES chats(id)
                )''')

    conn.commit()
    conn.close()

    init_db()

#Route setup
@app.route('/')
def home():
    pass

@app.route("")
def view_chat():
    pass

@app.route("/new_chat")
def new_chat():
    pass

@app.route("")
def send_mesaage():
    pass
    #python main
    if __name__=="__main__":
        app.run(debug=True)