import langchain
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

def load_model():
    load_dotenv()
    
    # Initialize the model
    llm_model = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.getenv('OPENAI_KEY'), temperature=0.3)
    return llm_model

def create_qa_bot():
    llm_model = load_model()
    
    # Intialize the loader. We use Directory loader to return all .txt files from a directory
    loader = DirectoryLoader('./textFiles', glob="**/*.txt")
    data = loader.load()
    
    # Split the documents into chunks for smaller context windows for the LLM
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    split_docs = text_splitter.split_documents(data)
    
    # Embedd and store those documents in a vector database
    # We use Chroma because it is free and open source!
    embedder = OpenAIEmbeddings(api_key=os.getenv('OPENAI_KEY'))
    vectorstore = Chroma.from_documents(documents=split_docs, embedding=embedder)

    # Set a retriever to retrieve our related documents!
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

def bot(human_message):
    llm_model = load_model()
    retriever = create_qa_bot()
    document_chain = define_document_chain()

    retrieved_docs = retriever.invoke(human_message)
    ans = document_chain.invoke(
        {
            "context": retrieved_docs,
            "messages": [
                HumanMessage(content=human_message)
            ],
        }
    )
    print(retrieved_docs)
    print(ans)
    
if __name__ == "__main__":
    human_message = input("Hi, how can I help you today? \n")
    bot(human_message)