from flask import Flask
import threading
import worker
import json
from bson import json_util
import datetime

app = Flask(__name__)


class state:
    status = []
    db_latest = []
    capacities = []
    stats = []


def update_state(new_status, new_db_latest, new_capacities, new_stats):
    state.status = json.dumps(new_status)
    state.db_latest = json_util.dumps(new_db_latest)
    state.capacities = json.dumps(new_capacities)
    state.stats = json.dumps(new_stats)


def background_worker():
    worker.start(update_state)


@app.route('/')
def index():
    body = {}
    body["date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body["status"] = json.loads(state.status)
    body["jobs"] = json.loads(state.db_latest)
    body["capacities"] = json.loads(state.capacities)
    body["stats"] = json.loads(state.stats)
    return json.dumps(body)


if __name__ == '__main__':
    thread = threading.Thread(target=background_worker)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
