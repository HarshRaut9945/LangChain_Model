from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage,AIMessage,SystemMessage
from dotenv import load_dotenv
import os

class LangChainClient:
    def __init__(self,mode='General'):
        role_prompts={
            "Code Analysis": "You are an expert code analyst. Break down and explain code clearly.",
            "Code Generator": "You are a senior developer. Generate high-quality, production-ready code.",
            "Debugger": "You are a debugging assistant. Find issues, explain them, and suggest fixes.",
            "Code Guide": "You are a mentor. Teach coding best practices step by step.",
            "Optimization": "You are a performance engineer. Optimize code for speed and efficiency.",
            "Explain Code": "You are a teacher. Explain code in simple terms with examples.",
            "Project Builder": "You are a full-stack developer. Build entire projects end-to-end.",
            "Documentation": "You are a technical writer. Generate professional documentation.",
            "General": "You are a full-stack developer assistant. Help with any coding tasks."
        }

        self.system_prompt =role_prompts.get