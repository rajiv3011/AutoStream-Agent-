from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from mistral_llm import generate_response
import json

# -----------------------
# Load knowledge base
# -----------------------
def load_documents():
    with open("knowledge.json") as f:
        data = json.load(f)

    docs = []

    for p in data["plans"]:
        text = f"{p['name']} plan costs {p['price']} and includes {p['features']}"
        docs.append(Document(page_content=text))

    for policy in data["policies"]:
        docs.append(Document(page_content=policy))

    return docs


# -----------------------
# Build vector store
# -----------------------
def create_vector_store():
    docs = load_documents()

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


# Initialize once
vectorstore = create_vector_store()

# -----------------------
# RAG Retrieval Function
# -----------------------
def retrieve(query):
    docs = vectorstore.similarity_search(query, k=3)

    context = "\n".join([d.page_content for d in docs])

    prompt = f"""
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {query}
    """

    response = generate_response(prompt)

    return response