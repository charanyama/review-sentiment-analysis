import os
from dotenv import load_dotenv
from app import app

load_dotenv()

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == "__main__":
    app.run(host=HOST or "0.0.0.0", port=PORT or 3000)
