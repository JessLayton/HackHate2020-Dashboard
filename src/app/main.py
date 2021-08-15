'''
Main app code, including routing.
'''
from flask import Flask, request
from validators import validate_reporting_numbers, validate_unreported_cases
from utilities import sort_and_group_by_quarter

app = Flask(__name__)


@app.route("/reportingNumbers", methods=['POST'])
def reporting_numbers() -> str:
    '''
    Return a dict to be used by the dashboard to display the data.

    Uses the JSend format.
    '''
    try:
        # Validate request JSON
        data = request.get_json()
        success, message = validate_reporting_numbers(data)
        # If request JSON is invalid, return a failure message.
        if not success:
            return {"status": "fail", "message": message}

        quarters = []

        for quarter_data in data:
            reported = quarter_data['reportingDetails']['reported']
            supported = quarter_data['reportingDetails']['supported']
            quarters.append(
                {
                    "quarter": quarter_data['quarter'],
                    "year": quarter_data["year"],
                    "reported": reported,
                    "supported": supported,
                    "totalHandled": reported + supported
                }
            )

        quarters = sort_and_group_by_quarter(quarters)
    except Exception as err:
        return {"status": "error", "message": repr(err)}

    return {"status": "success", "data": {"body": quarters}}


@app.route("/unreportedCases", methods=['POST'])
def unreported_cases() -> str:
    '''
    Return a dict to be used by the dashboard to display the data.

    Uses the JSend format.
    '''
    try:
        # Validate request JSON
        data = request.get_json()
        success, message = validate_unreported_cases(data)
        # If request JSON is invalid, return a failure message.
        if not success:
            return {"status": "fail", "message": message}

        quarters = []

        for quarter_data in data:
            quarter = {"quarter": quarter_data['quarter'], "year": quarter_data["year"]}
            quarter.update(quarter_data['unreportedCases'])
            quarters.append(quarter)

        quarters = sort_and_group_by_quarter(quarters)
    except Exception as err:
        return {"status": "error", "message": repr(err)}

    return {"status": "success", "data": {"body": quarters}}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
