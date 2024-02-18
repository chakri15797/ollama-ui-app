import io
from dash import html, dcc, Input, Output, State, Dash
from dash.exceptions import PreventUpdate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from tika import parser as tika_parser
import ollama

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Document Question Answering System"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    dcc.Input(id='question-input', type='text', placeholder='Enter your question...'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-div', style={'whiteSpace': 'pre-line', 'margin': '10px'})
])

# Define a function to process the uploaded documents and generate the response
def process_documents(contents, question):
    if contents is None or question is None:
        raise PreventUpdate

    documents = []
    for content in contents:
        content_type, content_string = content.split(',')
        # decoded = base64.b64decode(content_string)
        file_stream = io.BytesIO(content_string.encode('utf-8'))
        parsed = tika_parser.from_buffer(file_stream)
        text_content = parsed.get('content', '')
        documents.append(text_content)
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_text("\n\n".join(documents))
    embeddings = OllamaEmbeddings(model='mistral')
    vectorstore = Chroma.from_texts(texts=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    formatted_question = f"Question: {question}\n\n"
    response_temp = retriever.invoke(formatted_question)
    formatted_prompt = f"Question: {question}\n\nContext: {response_temp}"
    response = ollama.chat(model='mistral', messages=[{'role': 'user', 'content': formatted_prompt}])
    return response['message']['content']


# Define callback to process the uploaded data and question when the submit button is clicked
@app.callback(
    Output('output-div', 'children'),
    Input('submit-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('question-input', 'value')
)
def update_output(n_clicks, contents, question):
    if n_clicks > 0:
        op= process_documents(contents, question)
        print(op)
        return op
    raise PreventUpdate

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

