import os
import gradio as gr
import openai
from utils import helpers

openai.api_key = os.environ.get("OPENAI_API_KEY")

def healthcare_chat(user_id, user_input, file_upload=None):
    helpers.create_user(user_id)
    user = helpers.get_user(user_id)

    if not user["paid"]:
        return "⚠️ Free users must pay via Telebirr to unlock full chat."

    if not user_input.strip():
        return "Please type a message."

    uploaded_file_msg = f"\nUploaded file: {file_upload.name}" if file_upload else ""
    helpers.add_message(user_id, "user", user_input + uploaded_file_msg)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a healthcare AI assistant."},
                *user["conversation"]
            ],
            temperature=0.7,
            max_tokens=300
        )
        answer = response.choices[0].message['content'].strip()
    except Exception as e:
        answer = f"Error: {str(e)}"

    helpers.add_message(user_id, "assistant", answer)
    return answer

def pay(user_id):
    helpers.mark_paid(user_id)
    return "✅ Payment received! You are now a premium user."

def download_history(user_id):
    user = helpers.get_user(user_id)
    if not user:
        return "No history found."
    history = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in user["conversation"]])
    return history

# Gradio SaaS UI
with gr.Blocks(css=open("static/style.css").read()) as demo:

    # Homepage / Welcome
    with gr.Column():
        gr.Image("assets/logo.png", elem_id="logo", interactive=False)
        gr.Markdown("<h1>☕️ Welcome to Healthcare AI</h1>")
        gr.Markdown("""
        <p>Ask healthcare questions, upload lab reports, and get AI guidance.</p>
        <ul>
        <li>Premium chat with Telebirr payment</li>
        <li>Per-user conversation memory</li>
        <li>Downloadable chat transcripts</li>
        <li>Professional SaaS UI</li>
        </ul>
        <p>Scroll down to start chatting.</p>
        """)

    gr.Markdown("---")

    # Payment & Chat
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 💰 Payment Section")
            user_id_input = gr.Textbox(label="Your User ID", placeholder="Enter a unique ID")
            pay_button = gr.Button("Pay via Telebirr", variant="primary")
            pay_status = gr.Textbox(label="Payment Status", interactive=False)

        with gr.Column(scale=2):
            gr.Markdown("### 🩺 AI Chat")
            chat_user_input = gr.Textbox(label="Ask a healthcare question", placeholder="Type your question here...")
            chat_file_upload = gr.File(label="Upload lab report (optional)", file_types=[".pdf", ".png", ".jpg"])
            chat_output = gr.Textbox(label="AI Response", interactive=False)
            chat_button = gr.Button("Send", variant="primary")

    # Download history
    gr.Markdown("### 📄 Download Chat History")
    download_button = gr.Button("Download History", variant="secondary")
    download_output = gr.Textbox(label="History", interactive=False)

    # Event binding
    pay_button.click(fn=pay, inputs=user_id_input, outputs=pay_status)
    chat_button.click(fn=healthcare_chat, inputs=[user_id_input, chat_user_input, chat_file_upload], outputs=chat_output)
    download_button.click(fn=download_history, inputs=user_id_input, outputs=download_output)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False
    )
