'''
Tests for payload validators.
'''
import pytest
from app.validators import validate_reporting_numbers, validate_unreported_cases

class TestValidators:
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

    # reporting numbers

    def test_validate_reporting_numbers_success(self):
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert success
        assert msg == ''

    def test_validate_reporting_numbers_failure_negative_year(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][0], 'year', -1)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '-1 is less than or equal to the minimum of 0'

    def test_validate_reporting_numbers_failure_negative_quarter(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][0], 'quarter', -1)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '-1 is less than the minimum of 1'

    def test_validate_reporting_numbers_failure_quarter_over_four(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][0], 'quarter', 5)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '5 is greater than the maximum of 4'

    def test_validate_reporting_numbers_failure_negative_reported(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][0]['reportingDetails'], 'reported', -1)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '-1 is less than the minimum of 0'

    def test_validate_reporting_numbers_failure_negative_supported(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][0]['reportingDetails'], 'supported', -1)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '-1 is less than the minimum of 0'

    def test_validate_reporting_numbers_failure_empty_body(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data, 'body', [])
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == '[] is too short'

    def test_validate_reporting_numbers_failure_repeated_quarter(self, monkeypatch):
        monkeypatch.setitem(self.reporting_numbers_data['body'][1], 'quarter', 1)
        success, msg = validate_reporting_numbers(self.reporting_numbers_data)
        assert not success
        assert msg == 'Data for 2021 Q1 appears more than once'

    # unreported cases

    def test_validate_unreported_cases_success(self):
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert success
        assert msg == ''

    def test_validate_unreported_cases_failure_negative_year(self, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data['body'][0], 'year', -1)
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == '-1 is less than or equal to the minimum of 0'

    def test_validate_unreported_cases_failure_negative_quarter(self, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data['body'][0], 'quarter', -1)
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == '-1 is less than the minimum of 1'

    def test_validate_unreported_cases_failure_quarter_over_four(self, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data['body'][0], 'quarter', 5)
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == '5 is greater than the maximum of 4'

    @pytest.mark.parametrize('figure', ["lackEvidence", "notTrustPolice", "policeNotBelieve", "afraid", "abuseStop", "talk", "clientOther", "other"])
    def test_validate_unreported_cases_failure_negative_figure(self, figure, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data['body'][0]['unreportedCases'], figure, -1)
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == '-1 is less than the minimum of 0'

    def test_validate_unreported_cases_failure_empty_body(self, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data, 'body', [])
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == '[] is too short'

    def test_validate_unreported_cases_failure_repeated_quarter(self, monkeypatch):
        monkeypatch.setitem(self.unreported_cases_data['body'][1], 'quarter', 1)
        success, msg = validate_unreported_cases(self.unreported_cases_data)
        assert not success
        assert msg == 'Data for 2021 Q1 appears more than once'