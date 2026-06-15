from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from loguru import logger

def load_retriever(vectorstore_config:dict, retrieval_config:dict):
    hf = HuggingFaceEmbeddings(model_name = vectorstore_config["embedding_model"])
    vectorstore = Chroma(embedding_function= hf,persist_directory=vectorstore_config["persist_dir"])
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs= {"k":retrieval_config["top_k"],
                        "score_threshold":retrieval_config["score_threshold"]}
    )
    logger.info("Retriever loaded")
    return retriever


