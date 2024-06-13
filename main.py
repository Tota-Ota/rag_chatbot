from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from embedding import get_embedding_function
from langchain_community.vectorstores.chroma import Chroma
CHROMA_PATH = "chroma"
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 80,
        length_function = len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

loader = PyPDFLoader("data\policy-booklet-0923.pdf")
pages = loader.load_and_split()
chunks = split_documents(pages)
last_page_id = None
current_chunk_index = 0
for chunk in chunks:
    source = chunk.metadata.get("source")
    page = chunk.metadata.get("page")
    current_page_id = f"{source}:{page}"
    if current_page_id == last_page_id:
        current_chunk_index += 1
    else:
        current_chunk_index = 0
    chunk_id = f"{current_page_id}:{current_chunk_index}"
    last_page_id = current_page_id
    chunk.metadata["id"] = chunk_id
embedding_function = get_embedding_function()
db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_function
)

existing_items = db.get(include=[])
existing_ids = set(existing_items["ids"])
print(f"Number of existing documents in DB: {len(existing_ids)}")
new_chunks = []
for chunk in chunks:
    if chunk.metadata["id"] not in existing_ids:
        new_chunks.append(chunk)
new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
if len(new_chunks):
    print(f"Adding new documents: {len(new_chunks)}")
    new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    db.add_documents(new_chunks, ids=new_chunk_ids)
    db.persist()
else:
    print("No new documents to add")

