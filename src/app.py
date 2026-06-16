import os

import streamlit as st

from chain import build_chain, get_prompt, load_llm
from ingest import load_config
from retriever import load_retriever

CONFIG_PATH = os.getenv("CONFIG_PATH", "config.yaml")

st.title("ChatBot for CVS")

if "chain" not in st.session_state:
    config=load_config(CONFIG_PATH)
    retriever=load_retriever(config["vectorstore"],config["retrieval"])
    llm=load_llm(config["llm"])
    prompt=get_prompt()
    st.session_state["chain"]= build_chain(llm,retriever,prompt)

# Initialise la liste si elle n'existe pas
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Affiche chaque message
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

#Récuperer la question
if question := st.chat_input("Pose moi une question"):
    st.chat_message("user").write(question)

    # Appeler la chain
    response = st.session_state["chain"].invoke({"input": question})

    # Afficher la réponse
    st.chat_message("assistant").write(response["answer"])
    with st.expander("Sources utilisées"):
        for doc in response["context"]:
            source = doc.metadata['source']
            page = doc.metadata['page']
            content = doc.page_content[:200]
            st.info(f"**{source}** — page {page}\n\n{content}...")

    # 6. Sauvegarder dans l'historique
    st.session_state["messages"].append({"role": "user", "content": question})
    st.session_state["messages"].append(
        {"role": "assistant", "content":response["answer"]}
        )

