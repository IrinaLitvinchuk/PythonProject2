from unittest.mock import patch

from src.external_api import get_converted_amount


@patch("requests.request")
def test_get_converted_amount(mock_request):
    """"""
    mock_response = mock_request.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 100.0}

    transaction = {"operationAmount": {"amount": "10", "currency": {"code": "USD"}}}
    result = get_converted_amount(transaction)
    assert result == 100.0
