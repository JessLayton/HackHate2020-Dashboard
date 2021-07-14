'''
Validators for JSON request data sent to endpoints.
'''
from jsonschema import validate, ValidationError

REPORTING_NUMBERS_SCHEMA = {
    "type": "object",
    "properties": {
        "body": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "quarter": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "year": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "reportingDetails": {
                        "type": "object",
                        "properties": {
                            "reported": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "supported": {
                                "type": "integer",
                                "minimum": 0
                            }
                        },
                        "required": ["reported", "supported"]
                    }
                },
                "required": ["quarter", "year", "reportingDetails"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["body"]
}
UNREPORTED_CASES_SCHEMA = {
    "type": "object",
    "properties": {
        "body": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "quarter": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 4
                    },
                    "year": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "unreportedCases": {
                        "type": "object",
                        "properties": {
                            "lackEvidence": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "notTrustPolice": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "policeNotBelieve": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "afraid": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "abuseStop": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "talk": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "clientOther": {
                                "type": "integer",
                                "minimum": 0
                            },
                            "other": {
                                "type": "integer",
                                "minimum": 0
                            }                            
                        },
                        "required": [
                          "lackEvidence",
                          "notTrustPolice",
                          "policeNotBelieve",
                          "afraid",
                          "abuseStop",
                          "talk",
                          "clientOther",
                          "other"
                        ]
                    }
                },
                "required": ["quarter", "year", "unreportedCases"]
            },
            "minItems": 1,
            "uniqueItems": True
        }
    },
    "required": ["body"]
}


def validate_payload(data, schema):
    '''
    Returns `(True, '')` if `data` is  valid JSON for `schema` and has data
    specified for each quarter at most once. Otherwise, returns `(False, msg)`, where `msg` is
    a string explaining why `data` is invalid.

    :param data: A dict representing a JSON payload
    :type data: dict

    :param schema: A dict representing a jsonschema schema
    :type data: dict

    :returns: A tuple stating whether or not `data` is valid, and a reason why if it is not.
    :rtype: (bool, str)
    '''
    # Check if schema is valid
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        return (False, e.message)

    # Check if each year and quarter appears at most once.
    quarters = []
    for obj in data['body']:
        quarter = (obj['year'], obj['quarter'])
        if quarter not in quarters:
            quarters.append(quarter)
        else:
            # This quarter appears more than once, the payload is invalid.
            return (False, f"Data for {quarter[0]} Q{quarter[1]} appears more than once")

    # All checks passed, the payload is valid.
    return (True, '')


def validate_reporting_numbers(data):
    '''
    Returns `(True, '')` if `data` is a valid payload for the /reportingNumbers endpoint.

    :param data: A dict representing a JSON payload
    :type data: dict

    :returns: A tuple stating whether or not `data` is valid, and a reason why if it is not.
    :rtype: (bool, str)
    '''
    return validate_payload(data, REPORTING_NUMBERS_SCHEMA)


def validate_unreported_cases(data):
    '''
    Returns `(True, '')` if `data` is a valid payload for the /unreportedCases endpoint.

    :param data: A dict representing a JSON payload
    :type data: dict

    :returns: A tuple stating whether or not `data` is valid, and a reason why if it is not.
    :rtype: (bool, str)
    '''
    return validate_payload(data, UNREPORTED_CASES_SCHEMA)
