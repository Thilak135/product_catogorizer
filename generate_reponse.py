import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key = api_key)
generation_config = {
    "temperature" : 0.95,
    "top_k" : 1,
    "top_p" : 1
}

model = genai.GenerativeModel(
    model_name = "gemini-1.5-pro-latest",
    generation_config = generation_config
)

prompt = """
***Using the below list of values and the query, provide me the best matching answer from the list.
Do not provide any unnecessary information. Only give me a one word answer which exists in the list.
There is definetly an answer in the list so , try to find the best matching reponse from the list.***

query = {query}
list = {document}

The Matching Response:
""" 

response = model.generate_content([prompt])

print(response)