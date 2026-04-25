import gradio as gr
from utils import *


def process(url):
    if not url:
        return "", "Please enter a URL", ""

    video_id = extract_video_id(url)
    text = get_transcript(video_id)

    if "not available" in text.lower():
        return "", text, ""

    summary = summarize_text(text)
    article = generate_article(summary)

    return f"YouTube Video ({video_id})", summary, article


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎥 YouTube → Article Generator (GenAI)")
    gr.Markdown("Convert YouTube videos into summaries and structured articles")

    url = gr.Textbox(label="Enter YouTube URL")
    btn = gr.Button("Generate", variant="primary")

    #  Removed thumbnail
    title = gr.Textbox(label="Video Title")

    summary = gr.Textbox(label="Summary", lines=8)
    article = gr.Markdown(label="Generated Article")

    btn.click(
        process,
        inputs=url,
        outputs=[title, summary, article]
    )

demo.launch(server_name="0.0.0.0", server_port=7860, ssr_mode=False)
