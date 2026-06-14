# Take the PDF files and convert them to text files then ingest the text files into the database.

import yaml
from loguru import logger
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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
        logger.error("No document to chunk")
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


@click.command()
@click.option('--config','-c','config')
def main(config):
        config_loaded=load_config(config)
        pdfs_loaded=load_documents_from_directory(config_loaded["data"]["source_dir"])
        chunk_documents(pdfs_loaded,config_loaded["chunking"])
       

if __name__ == "__main__":
    main()
