import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb


db_chroma_path = "vectorstores/db_chroma"
def jsonloader(file_path):
    with open(r"D:\catogorize rag\Taxonomy-Fashion.json", 'r') as file:
        data = json.load(file)
    print(data)

    documents = []
    index = 1
    for i in data:
        documents.append(i["Sub-Category"])
    print(documents)
    remove = []
    ids = []
    for dict in data:
        temp_dict = {}
        flag = 0
        for key in dict:
            if dict[key] != 'O':
                flag += 1
                temp_dict[key] = dict[key]
        if flag:
            remove.append(temp_dict)
            ids.append(str(index))
            index += 1
    print(remove)
    return remove,documents , ids



def get_embeddings(documents):
    embedding_function = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",  
    model_kwargs={"device": "cpu" , "trust_remote_code":True}  
    )
    embedings=[]
    for i in documents:
        embedings.append(embedding_function.embed_query(i))

    return embedings




def create_store():
    remove , documents , ids = jsonloader("Taxonomy-Fashion.json")
    embeddings=get_embeddings(documents)
    client = chromadb.PersistentClient(path=db_chroma_path)

    collection = client.create_collection(
        name="db_chroma_path",
        metadata={"hnsw:space": "cosine"} # l2 is the default
    )


    collection.add(
    documents=documents,
    metadatas=remove,
    embeddings=embeddings,
    ids = ids,
    )
    

if __name__ == "__main__":
    create_store()