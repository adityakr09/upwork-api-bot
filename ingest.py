from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "API_Documentation_Partial.pdf"
CHROMA_DIR = "./chroma_store"


def load_pdf(path):
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    return full_text


def main():
    print("Loading PDF...")
    text = load_pdf(PDF_PATH)

    # Sanity Check (Part A1)
    print(f"\n--- Sanity Check ---")
    print(f"Total characters: {len(text)}")
    print(f"Sample text:\n{text[:300]}\n")

    # Chunking (Part A2)
    
    # from the previous one, preventing loss of meaning at chunk boundaries.
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    print(f"Total chunks created: {len(chunks)}")

    # Embedding + storing in ChromaDB (Part A3)
    print("\nEmbedding and storing in ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma.from_texts(chunks, embedding=embeddings, persist_directory=CHROMA_DIR)
    vectorstore.persist()

    print(f"\nDone! Vector store saved to: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
