import os
import google.generativeai as genai
import gradio as gr
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=API_KEY)


class ChatBot:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def chat(self, message, image):
        try:
            # Case 1: text + image
            if message and image:
                img = Image.open(image)
                response = self.model.generate_content([message, img])

            # Case 2: only image
            elif image:
                img = Image.open(image)
                response = self.model.generate_content(
                    ["Describe this image in detail", img]
                )

            # Case 3: only text
            elif message:
                response = self.model.generate_content(message)

            else:
                return "Please provide text or image"

            return response.text

        except Exception as e:
            return f"Error: {str(e)}"


bot = ChatBot()

demo = gr.ChatInterface(
    fn=bot.chat,
    title="Gemini Image + Text Chatbot",
    description="Ask anything or upload an image",
)

if __name__ == "__main__":
    demo.launch()
