import gradio as gr
import binascii
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import ollama
import base64
import io
from tika import parser as tika_parser

def load_and_retrieve_docs(file, question):
    try:
        file_stream = io.BytesIO(file.encode('utf-8'))
        parsed = tika_parser.from_buffer(file_stream)
        text_content = parsed.get('content', '')

        if text_content is None:
            return "Error: Failed to extract text content from the uploaded document."

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_text(text_content)

        embeddings = OllamaEmbeddings(model="mistral")
        vectorstore = Chroma.from_texts(texts=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        response_temp = retriever.invoke(question)
        formatted_prompt = f"Question: {question}\n\nContext: {response_temp}"
        response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
        return response['message']['content']

    except binascii.Error:
        return "Error: Invalid base64 string format."


# Gradio interface
iface = gr.Interface(
    fn=load_and_retrieve_docs,
    inputs=[
        gr.File(label="Upload Document"),
        gr.Textbox(label="Question")
    ],
    outputs=gr.Textbox(label="Answer"),
    title="Document Question Answering System",
    description="Upload a document and ask a question about it."
)

# Launch the app
iface.launch()


