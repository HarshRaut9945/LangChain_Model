import google.generativeai as genai
import gradio as gr
import os
from dotenv import load_dotenv

load_dotenv()


class ChatBot:
    def __init__(self):
        self.model_name = "gemini-2.5-flash"
        self.temperature = 0
        self.api_key = os.getenv("GOOGLE_API_KEY")

        genai.configure(api_key=self.api_key)
        self.load_model()

    def load_model(self):
        self.llm = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={"temperature": self.temperature},
        )

    # ✅ renamed to chat
    def chat(self, message, history):
        try:
            response = self.llm.generate_content(message)
            return response.text if response.text else "No response generated."
        except Exception as e:
            return f"Error: {str(e)}"


bot = ChatBot()

demo = gr.ChatInterface(
    fn=bot.chat,
    title="Gemini Chatbot",
    description="Ask anything",
)

if __name__ == "__main__":
    demo.launch()
