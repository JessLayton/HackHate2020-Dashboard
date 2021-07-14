import json
import pytest
from flask import Flask
from app.main import reporting_numbers, unreported_cases, app


@pytest.fixture
def client():
    return app.test_client()

class TestEndpoints:
    reporting_numbers_data = {
        'body': [
            {
                "year": 2021,
                "quarter": 1,
                "reportingDetails": {
                    "reported": 6,
                    "supported": 7
                }
            },
            {
                "year": 2021,
                "quarter": 2,
                "reportingDetails": {
                    "reported": 0,
                    "supported": 1
                }
            }
        ]
    }

    unreported_cases_data = {
        'body': [
            {
                "year": 2021,
                "quarter": 1,
                "unreportedCases": {
                    "lackEvidence": 0,
                    "notTrustPolice": 1,
                    "policeNotBelieve": 5,
                    "afraid": 2,
                    "abuseStop": 7,
                    "talk": 9,
                    "clientOther": 4,
                    "other": 0
                }
            },
            {
                "year": 2021,
                "quarter": 2,
                "unreportedCases": {
                    "lackEvidence": 2,
                    "notTrustPolice": 1,
                    "policeNotBelieve": 2,
                    "afraid": 2,
                    "abuseStop": 7,
                    "talk": 9,
                    "clientOther": 4,
                    "other": 0
                }
            }
        ]
    }

    def test_reporting_numbers_success(self, client):
        response = client.post(
            '/reportingNumbers',
            data=json.dumps(self.reporting_numbers_data),
            content_type='application/json'
        )

        resp_data = response.get_json()

        assert resp_data['status'] == 'success'
        assert resp_data['data'] == {
            "body": [
                {
                    "quarter": "Q1 2021",
                    "reported": 6,
                    "supported": 7,
                    "totalHandled": 13
                },
                {
                    "quarter": "Q2 2021",
                    "reported": 0,
                    "supported":1,
                    "totalHandled": 1
                }
            ],
        }

    def test_reporting_numbers_failure_validation(self, client, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data, 'body', [])
        response = client.post(
            '/reportingNumbers',
            data=json.dumps(self.reporting_numbers_data),
            content_type='application/json'
        )

        resp_data = response.get_json()

        assert resp_data['status'] == 'fail'
        assert resp_data['message'] == '[] is too short'

    def test_unreported_cases_success(self, client):
        response = client.post(
            '/unreportedCases',
            data=json.dumps(self.unreported_cases_data),
            content_type='application/json'
        )

        resp_data = response.get_json()

        assert resp_data['status'] == 'success'
        assert resp_data['data'] == {
            "body": [
                {
                    "quarter": "Q1 2021",
                    "lackEvidence": 0,
                    "notTrustPolice": 1,
                    "policeNotBelieve": 5,
                    "afraid": 2,
                    "abuseStop": 7,
                    "talk": 9,
                    "clientOther": 4,
                    "other": 0
                },
                {
                    "quarter": "Q2 2021",
                    "lackEvidence": 2,
                    "notTrustPolice": 1,
                    "policeNotBelieve": 2,
                    "afraid": 2,
                    "abuseStop": 7,
                    "talk": 9,
                    "clientOther": 4,
                    "other": 0
                }
            ],
        }

    def test_unreported_cases_failure_validation(self, client, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data, 'body', [])
        response = client.post(
            '/unreportedCases',
            data=json.dumps(self.unreported_cases_data),
            content_type='application/json'
        )

        resp_data = response.get_json()

        assert resp_data['status'] == 'fail'
        assert resp_data['message'] == '[] is too short'

    def test_reporting_numbers_failure_get_request(self, client):
        response = client.get(
            '/reportingNumbers',
            data=json.dumps(self.unreported_cases_data),
            content_type='application/json'
        )

        assert response.status_code == 405å

    def test_unreported_cases_failure_get_request(self, client):
        response = client.get(
            '/unreportedCases',
            data=json.dumps(self.unreported_cases_data),
            content_type='application/json'
        )

        assert response.status_code == 405