from pathlib import Path

from langchain.text_splitter import TokenTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# get temp path
# from tempfile import gettempdir


folder = Path(__file__).parent / "tmp"

loader = DirectoryLoader(
    path=folder,
    glob="*.md",
    loader_cls=UnstructuredMarkdownLoader,
    loader_kwargs={"strategy": "fast"},
    use_multithreading=True,
)


def test_load():
    raw_documents = loader.load()

    spliter = TokenTextSplitter(encoding_name="cl100k_base", chunk_size=6000, chunk_overlap=0)
    documents = spliter.split_documents(documents=raw_documents)
    db = FAISS.from_documents(documents, OpenAIEmbeddings())

    query = "based on the information provided, what is the job title of the vacancy?"

    results = db.similarity_search(query=query)

    print(results)


test_load()
