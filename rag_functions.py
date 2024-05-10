import google.generativeai as genai
import chromadb
import dotenv
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
dotenv.load_dotenv()

class Ragfunctions:
    '''
    This class implements retrieval augumented generation process.
    '''
    def __init__(self):
        '''
        This function loads the Gemini Model, Embedding Model, and Vector Database Collection
        '''
        self.db_path = "vectorstores/db_chroma"
        self.collection_name = "db_chroma_path"
        self.gemini_model_name = "gemini-1.5-pro-latest"
        self.model = "nomic-ai/nomic-embed-text-v1.5"
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.generative_config = {
            'temperature' : 0.75,
            'top_k' : 1,
            'top_p' : 1
        }
        self.client = chromadb.PersistentClient(self.db_path)
        genai.configure(api_key = self.api_key)
        self.model = genai.GenerativeModel(
            model_name = self.gemini_model_name,
            generation_config = self.generative_config
        )

        self.embedding_model = HuggingFaceEmbeddings(
           model_name="nomic-ai/nomic-embed-text-v1.5",  
           model_kwargs={"device": "cpu" , "trust_remote_code":True}
        )

        self.collection = self.client.get_collection(self.collection_name)

    def get_query_documents(self , query):
        '''
        This function returns the query documents and their metadatas as a list by querying with query provided by the user
        '''
        query_embeddings = self.embedding_model.embed_query(query)
        documents = self.collection.query(query_embeddings , n_results=3)

        document_list = documents['documents'][0]
        metadatas = documents['metadatas'][0]

        return document_list , metadatas
    

    def initiate_querying(self , query):
        '''
        This function implements get_query_documents to get documents and metadatas. Then the query and documents are used to
        extract the best matching document name for the given query and returns it's meta data
        '''
        documents , metadatas = self.get_query_documents(query)
        prompt = f"""
        ***Using the below list of values and the query, provide me the best matching answer from the list.
        Do not provide any unnecessary information. Only give me a one word answer which exists in the list.
        There is definetly an answer in the list so , try to find the best matching reponse from the list.***

        query = {query}
        list = {documents}

        The Matching Response:
        """

        response = self.model.generate_content([
            prompt
        ])
        # print(documents)
        result = []
        # print(response.text)
        for i in metadatas:
            print(i['Sub-Category'])
            print(response.text)
            if (str(i['Sub-Category']) == (str(response.text).strip())):
                result.append(i)
                

        return result[0]


