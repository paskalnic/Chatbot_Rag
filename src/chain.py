from langchain_ollama import ChatOllama
from loguru import logger
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain.chains import create_retrieval_chain

# cle api http://localhost:11434/api
def load_llm(llm_config:dict):
    llm = ChatOllama(
        model= llm_config["model"],
        temperature= llm_config["temperature"],
        num_predict=llm_config["max_tokens"]
    )
    logger.info("Llm loaded")
    return llm

def get_prompt():
    messages = [
    (
        "system",
        """ 
        Tu es un assistant expert en analyse de CVs. 
        Réponds UNIQUEMENT à partir du contexte fourni. 
        Réponds toujours en français. 
        Si la réponse n'est pas dans le contexte, 
        dis clairement que tu ne trouves pas l'information.
        """,
    ),
    ("human","Contexte : {context}\n\nQuestion : {question}")
]
    prompt=ChatPromptTemplate.from_messages(messages)
    return prompt

def build_chain(llm,retriever,prompt):
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, question_answer_chain)
    logger.info("Chain built successfully")
    return chain