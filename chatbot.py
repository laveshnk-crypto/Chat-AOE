import os
from dotenv import load_dotenv
import gradio as gr
import time

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_community.document_loaders.url_selenium import SeleniumURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

openai_api_key = os.getenv('OPENAI_KEY')

def load_model():
    load_dotenv()
    
    # Initialize the model
    llm_model = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=openai_api_key, temperature=0.3)
    return llm_model

def create_qa_bot():    
    # Initialize the loader. We use Directory loader to return all .txt files from a directory
    loader = DirectoryLoader('./textFiles', glob="**/*.txt")
    data = loader.load()
    
    # Split the documents into chunks for smaller context windows for the LLM
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(data)
    
    # Embed and store those documents in a vector database
    # We use Chroma because it is free and open source!
    embedder = OpenAIEmbeddings(api_key=openai_api_key)
    vectorstore = Chroma.from_documents(documents=split_docs, embedding=embedder)

    # Set a retriever to retrieve our related documents
    retriever = vectorstore.as_retriever(k=4)
    
    return retriever

def define_document_chain():
    llm_model = load_model()
    
    # Defining the prompt
    System_Template = """
    You are Chat-AOE, a friendly chatbot assistant designed to answer questions about Age of Empires 2: Definitive edition.
    Answer the user's questions based on the below context related to the game.
    
    <context>
    {context}
    </context>
    """
    
    aoe_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                System_Template,
            ),
            MessagesPlaceholder(variable_name="messages")
        ]
    )
    
    # Defining our document chain
    document_chain = create_stuff_documents_chain(llm_model, aoe_prompt)
    
    return document_chain

def chat(message, history):
    retrieved_docs = retriever.invoke(message)
    ans = document_chain.invoke(
        {
            "context": retrieved_docs,
            "messages": [HumanMessage(content=message)],
        }
    )
    for i in range(len(ans)):
        time.sleep(0.008)  # Delay to simulate processing time
        yield ans[:i+1]

retriever = create_qa_bot()
document_chain = define_document_chain()

iface = gr.ChatInterface(chat, theme='ParityError/Anime')
iface.launch()