import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="City Tech CST Professor Guide") as demo:
    gr.Markdown("# 🎓 City Tech CST Unofficial Professor Guide")
    gr.Markdown("Ask questions about CST professors based on real student reviews from Rate My Professors.")
    
    with gr.Row():
        inp = gr.Textbox(
            label="Your Question",
            placeholder="e.g. What do students say about Suman Kalia's workload?",
            lines=2
        )
    
    btn = gr.Button("Ask", variant="primary")
    
    with gr.Row():
        answer = gr.Textbox(label="Answer", lines=8)
        sources = gr.Textbox(label="Sources", lines=8)
    
    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
