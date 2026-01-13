from unittest.mock import patch, MagicMock

from monitor import check_site


@patch('monitor.requests.get')
def test_check_site_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    assert check_site("https://fakexample.com") is True


@patch('monitor.requests.get')
def test_check_site_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    assert check_site("https://fakexample.com") is False
    