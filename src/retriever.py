from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from loguru import logger


def load_retriever(vectorstore_config:dict, retrieval_config:dict):
    hf = HuggingFaceEmbeddings(model_name = vectorstore_config["embedding_model"])
    vectorstore = Chroma(
        embedding_function= hf,
        persist_directory=vectorstore_config["persist_dir"]
        )
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs= {"k":retrieval_config["top_k"],
                        }
    )
    logger.info("Retriever loaded")
    return retriever


