import gradio as gr
import google.generativeai as genai
import base64

# 🔑 SET YOUR GEMINI API KEY
genai.configure(api_key="YOUR_GEMINI_API_KEY")

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")


def format_message(message):
    """
    Convert Gradio message (text + files) → Gemini parts format
    """
    parts = []

    # Text
    if message.get("text"):
        parts.append({"text": message["text"]})

    # Images
    if message.get("files"):
        for file_path in message["files"]:
            with open(file_path, "rb") as f:
                img_bytes = f.read()

            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": base64.b64encode(img_bytes).decode()
                }
            })

    return parts


def chat_fn(message, history):
    """
    Main chat function for Gradio
    """
    try:
        parts = format_message(message)

        response = model.generate_content(parts)

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"


# 🎨 Gradio UI
demo = gr.ChatInterface(
    fn=chat_fn,
    multimodal=True,
    title="Gemini Multimodal Chatbot",
    description="Chat with Gemini using text and images"
)

if __name__ == "__main__":
    demo.launch()
