'''
Main app code, including routing.
'''
from flask import Flask
import validators

app = Flask(__name__)


@app.route("/reportingNumbers", methods=['POST'])
def reporting_numbers() -> str:
    '''
    Return a dict to be used by the dashboard to display the data.
    '''
    # Validate request JSON
    data = request.get_json()
    validators.validate_reporting_numbers(data)

    quarters = []

    for quarter_data in sorted(data['body'], key=lambda x: (x['year'], x['quarter')]:
        quarter_text = f"Q{quarter_data['quarter'] quarter_data['year']"
        reported = quarter_data['reportingDetails']['reported']
        supported = quarter_data['reportingDetails']['supported']
        quarters.append(
            {
                "quarter": quarter_text,
                "reported": reported,
                "supported": supported,
                "totalHandled": reported + supported
            }
        )

    return {"data": quarters}


@app.route("/unreportedCases", methods=['POST'])
def unreported_cases() -> str:
    '''
    Return a dict to be used by the dashboard to display the data.
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
