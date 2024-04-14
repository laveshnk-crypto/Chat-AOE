import gradio as gr

def temp(messages, history):
    return "Hi there!!!"

interface = gr.ChatInterface(temp, theme='ParityError/Anime').launch()

with gr.Blocks() as block:
    interface.render()
    block.load(
        None,
        None,
        _js="""
        (function() {
            const params = new URLSearchParams(window.location.search);
            if (!params.has('__theme')) {
                params.set('__theme', 'light');
                window.location.search = params.toString();
            }
        })();
        """,
    )

block.launch(share=False)
