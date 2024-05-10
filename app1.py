import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
import transformers



def get_k_documents(query):
    client = chromadb.PersistentClient(path = "vectorstores/db_chroma")

    collection = client.get_collection(
        name = "db_chroma_path"
    )

    embedding_function = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1.5",  
        model_kwargs={"device": "cpu" , "trust_remote_code":True}
    )

    query_embeddings = embedding_function.embed_query(query)

    response_documents = collection.query(query_embeddings , n_results = 3)

    print(response_documents)
    

#     top_results = []
#     length = len(response_documents['ids'][0])
#     for i in range(0 , length):
#       sub_category = response_documents['documents'][0][i]
#       metadata = response_documents['metadatas'][0][i]
#       top_results.append({
#         'sub_category' : sub_category,
#         'metadatas' : metadata
#       })

#     data = {"query": query, "top_results": top_results}

#   # Load the LLM (assuming transformers library supports LLama-2)

#     llm = transformers.AutoModelForSeq2SeqLM.from_pretrained(r"D:\catogorize rag\llama-2-7b-chat.ggmlv3.q8_0.bin")
#     tokenizer = transformers.AutoTokenizer.from_pretrained(r"D:\catogorize rag\llama-2-7b-chat.ggmlv3.q8_0.bin")
#   # Indicate failure to load LLM

#   # Refine results using LLM (replace with your specific refinement logic)
#   # This is a placeholder example, modify based on your LLM's capabilities
#     prompt = f"Given the query '{query}' and the following top results, which result is the most relevant and informative?\n"
#     for i, result in enumerate(top_results):
#       prompt += f"{i+1}. {result['title']}: {result['content']}\n"

#     input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
#     output = llm.generate(input_ids, max_length=512, temperature=0.5)  # Adjust parameters as needed
#     refined_result_id = int(output[0][0].split()[1])  # Assuming output format indicates best result index

#     return response_documents[refined_result_id]


# if __name__ == "__main__":
#   query = input()
#   best_response = get_k_documents(query)
#   if best_response:
#     print(f"Best Result: {best_response['metadata']['title']}")
#     print(f"Content: {best_response['metadata']['content']}")
#   else:
#     print("Failed to refine results. Consider using a cloud-based LLM API or a supported model.")
    