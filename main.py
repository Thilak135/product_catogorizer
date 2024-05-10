from rag_functions import Ragfunctions
from flask import Flask, render_template, request

app = Flask(__name__)
r = Ragfunctions()

@app.get("/")
def index():
    return render_template("home.html")

@app.post('/get_query')
def query():
    try:
        data = request.get_json()
        print(data)
        response = r.initiate_querying(data['query'])
        return {'status':True, 'response': response}, 200
    except Exception as e:
        return {'status':False, 'message':str(e)}, 404
    
if __name__ == "__main__":
    app.run(debug=True, port=10000, host="0.0.0.0")