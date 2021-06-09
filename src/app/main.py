# -*- coding: utf-8 -*-

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/reportingNumbers", methods=['POST'])
def index() -> str:
    # transform a dict into an application/json response 
    return jsonify({"message": "Reporting numbers works"})

@app.route("/unreportedCases", methods=['POST'])
def index() -> str:
    # transform a dict into an application/json response 
    return jsonify({"message": "Unreported cases works"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)