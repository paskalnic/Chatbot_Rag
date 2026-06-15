from src.ingest import load_config,load_documents_from_directory,chunk_documents
from unittest.mock import patch,mock_open,Mock
from langchain_core.documents import Document

@patch("builtins.open",mock_open(read_data="data:\n source_dir: ./data/raw"))
def test_load_config():
    config=load_config("fake.yaml")
    assert config["data"]["source_dir"]=="./data/raw"


def test_chunk_documents():
    #Fake doc with 1245 characters
    fake_docs= [Document(page_content="a" * 1245)]
    chunk_config = {"chunk_size": 500, "chunk_overlap": 50}
    chunks_fake_docs=chunk_documents(fake_docs,chunk_config)
    assert len(chunks_fake_docs) > 1
    # all is used to  verify that all the elements respect the assert and also
    # we use <=600 because chunk size at 500 means we use 500 tokens max and one
    # token can be 4 characters

    assert all(len(chunk.page_content) <= 600 for chunk in chunks_fake_docs)

   
