from unittest.mock import patch, MagicMock
from src.check import check_site 


@patch('src.check.requests.get')
def test_check_site_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result, info = check_site("https://fakexample.com")
    
    assert result is True
    assert info == "200"


@patch('src.check.requests.get')
def test_check_site_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result, info = check_site("https://fakexample.com")

    assert result is False
    assert info == "Status: 404"


@patch('src.check.requests.get')
def test_check_site_exception(mock_get):
    import requests
    mock_get.side_effect = requests.exceptions.RequestException("booom")

    result, info = check_site("https://fakexample.com")

    assert result is False
    assert info == "Error"