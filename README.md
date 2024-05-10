# Product Catogorizer


 create a virtual environment
 
    python3 -m venv venv


activate virtual envirnoment

    venv/Scripts/activate     # For windows
     venv/bin/activate       # For Mac/Linux

install requirements

    pip install requirements.txt

Edit your rename .env.example to .env

        ren .env.example .env   # for windows
        mv .env.example .env    # For linux/Mac

Create embeddeds to store in chroma DB

    python ingest.py

run application by typing

    python main.py

the application runs in <a href="http://localhost:10000/">Home Page</a>
