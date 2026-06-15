# Take the PDF files and convert them to text files then ingest the text files into the database.

import yaml
from loguru import logger
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import click

def load_config(config_path:str) -> dict:
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Config file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise
    return config


def load_documents_from_directory(pdf_directory: str) -> list:

    try :
        loader = PyPDFDirectoryLoader(
        path= pdf_directory
        )
        documents:list = loader.load()
    except FileNotFoundError:
        logger.error(f"Directory not found : {pdf_directory}")
        raise
    logger.info(f"Documents loaded : {len(documents)}")
    return documents



def chunk_documents(documents:list, chunk_config:dict) -> list:
    if not documents:
        logger.error("No documents to chunk")
        raise ValueError("No documents to chunk")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_config["chunk_size"],
        chunk_overlap = chunk_config["chunk_overlap"])
    try:
        chunks_documents =text_splitter.split_documents(documents)
        logger.info(f"Documents chunked : {len(chunks_documents)}")
    except Exception as e:
        logger.error(f"Error Chunking Documents: {e}")
        raise

    return chunks_documents


def build_vectorstore(chunks:list, vectorstore_config:dict):
    if not chunks:
        logger.error("No chunks to embed")
        raise ValueError("No chunks to embed")
    
    hf = HuggingFaceEmbeddings(
        model_name=vectorstore_config["embedding_model"]
    )
   
    vectorstore = Chroma.from_documents (
        documents = chunks,
        embedding = hf,
        persist_directory = vectorstore_config["persist_dir"])
    logger.info(f"Vectorstore created at {vectorstore_config['persist_dir']}")



@click.command()
@click.option('--config','-c','config')
def main(config):
        config_loaded=load_config(config)
        pdfs_loaded=load_documents_from_directory(config_loaded["data"]["source_dir"])
        documents_chunked=chunk_documents(pdfs_loaded,config_loaded["chunking"])
        build_vectorstore(documents_chunked,config_loaded["vectorstore"])

       

if __name__ == "__main__":
    main()
