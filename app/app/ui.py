import gradio as gr
import requests

API_URL = "/chat"

def respond(message, history):
    r = requests.post(API_URL, json={"message": message})
    history.append((message, r.json()["response"]))
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("## 🏥 Healthcare AI Prototype")
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(server_name="0.0.0.0", server_port=8000)
