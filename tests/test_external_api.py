from unittest.mock import Mock, patch

import pytest

from src.external_api import get_converted_amount


@patch("requests.request")
def test_successful_usd_conversion(mock_request: Mock, sample_transaction_usd: dict) -> None:
    """Тестирование успешной конвертации USD в рубли."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7937.5}
    mock_request.return_value = mock_response

    result = get_converted_amount(sample_transaction_usd)
    assert result == 7937.5


@patch("requests.request")
def test_successful_eur_conversion(mock_request: Mock, sample_transaction_eur: dict) -> None:
    """Тестирование успешной конвертации EUR в рубли."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 9106.6}
    mock_request.return_value = mock_response

    result = get_converted_amount(sample_transaction_eur)
    assert result == 9106.6


def test_no_conversion_needed(sample_transaction_rub: dict) -> None:
    """Тест без конвертации (валюта уже в рублях)."""
    result = get_converted_amount(sample_transaction_rub)
    assert result == 100


@patch("requests.request")
def test_api_request_failure(mock_request: Mock, sample_transaction_usd: dict) -> None:
    """обработка ситуации, когда API возвращает ошибку (например, код 400)."""

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"
    mock_request.return_value = mock_response

    # Ожидаем выброс исключения
    with pytest.raises(Exception) as exception_info:
        get_converted_amount(sample_transaction_usd)
    # Проверяем сообщение исключения
    assert str(exception_info.value) == "Request failed with status code 400: Bad request"


def test_invalid_currency(invalid_transaction: dict) -> None:
    """Тестирование случая, когда валюта неизвестна или некорректна (например, XXX)."""
    result = get_converted_amount(invalid_transaction)
    assert result == 100
