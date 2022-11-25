import random
import string
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.http import httputil
from src.misc import updatewifipassword

_WIFI_PASSWORD = 'xwAERWqefV7cZPqvsUYs1CMZj4fD2acLl7V4SpHsPmr5zsbDdoxWXqVp43lOemu'


@patch('random.choices', MagicMock(return_value=list(_WIFI_PASSWORD)))
@patch('src.http.httputil.get_result', MagicMock(return_value=None))
@patch('builtins.print', MagicMock(return_value=None))
class TestUpdateWifiPassword(TestCase):

  def test(self) -> None:
    updatewifipassword.update_wifi_password()

    random.choices.assert_called_once_with(string.ascii_letters + string.digits, k=63)
    httputil.get_result.assert_called_once_with('setwifi.cgi', {'wifikey': _WIFI_PASSWORD})
    print.assert_called_once_with('new wi-fi password: ' + _WIFI_PASSWORD)
