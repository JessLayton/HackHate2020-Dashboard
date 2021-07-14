'''
Main app code, including routing.
'''
from flask import Flask

app = Flask(__name__)


@app.route("/reportingNumbers", methods=['POST'])
def reporting_numbers() -> str:
    # transform a dict into an application/json response 
    return {"message": "Reporting numbers works"}

@app.route("/unreportedCases", methods=['POST'])
def unreported_cases() -> str:
    # transform a dict into an application/json response 
    return {"message": "Unreported cases works"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
