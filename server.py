from flask import Flask
import threading
import worker
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

status = []

def update_state(new_status):
    status = new_status
    print(status)
    print("UPDATED!")

def background_worker():
    worker.start(update_state)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    thread = threading.Thread(target=background_worker)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)