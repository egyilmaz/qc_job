from flask import Flask
from handlers import submit, query

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit_handler():
    return submit()

@app.route('/query', methods=['GET'])
def query_handler():
    return query()
