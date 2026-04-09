import gradio as gr
import google.generativeai as genai

# Configuration de l'API
genai.configure(api_key="AIzaSyAgNvD3r9uPsRjz4uDgNAjtOmhTrpZcIZo")
model = genai.GenerativeModel('gemini-pro')

# Tes instructions strictes
SYSTEM_PROMPT = "Tu es MonIA. Réponds toujours de façon claire, courte, avec beaucoup d'emoji, et fais TOUJOURS une conclusion à la fin de la discussion. 🚀"

# Mémoire des discussions
chats = {"Discussion 1": []}

def monia_chat(msg, history, active_chat):
    if not msg: return "", history
    
    full_prompt = f"{SYSTEM_PROMPT}\n\nUtilisateur: {msg}"
    
    try:
        # Stream pour une réponse ultra-rapide
        response = model.generate_content(full_prompt, stream=True)
        history.append((msg, ""))
        for chunk in response:
            history[-1] = (msg, history[-1][1] + chunk.text)
            yield "", history
        chats[active_chat] = history
    except:
        yield "", history + [(msg, "⚠️ Erreur réseau. Réessaie !")]

def add_page():
    name = f"Discussion {len(chats) + 1} ✨"
    chats[name] = []
    return gr.update(choices=list(chats.keys()), value=name), []

# L'interface que tu as validée
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    with gr.Sidebar(label="Menu", open=False):
        gr.Markdown("### 📂 Pages")
        selector = gr.Dropdown(list(chats.keys()), value="Discussion 1", label="Changer de chat")
        gr.Button("+ Nouvelle Page").click(add_page, None, [selector, gr.Chatbot()])
        
    gr.Markdown("## 🤖 MonIA Pro")
    chatbot = gr.Chatbot(height=600, bubble_full_width=False)
    
    with gr.Row(variant="compact"):
        txt = gr.Textbox(placeholder="Écris ton message...", scale=9, container=False)
        btn = gr.Button("✈️", scale=1, variant="primary")

    btn.click(monia_chat, [txt, chatbot, selector], [txt, chatbot])
    txt.submit(monia_chat, [txt, chatbot, selector], [txt, chatbot])
    selector.change(lambda x: chats.get(x, []), selector, chatbot)

demo.queue()
demo.launch()
