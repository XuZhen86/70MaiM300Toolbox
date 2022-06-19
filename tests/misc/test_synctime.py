import datetime
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.http import httputil
from src.misc import synctime


@patch('datetime.datetime',
       SimpleNamespace(now=MagicMock(return_value=SimpleNamespace(strftime=MagicMock(
           return_value='20220611021555')))))
@patch('src.http.httputil.get_result', MagicMock(return_value=None))
class TestSyncTime(TestCase):

  def test(self):
    synctime.sync_time()

    datetime.datetime.now().strftime.assert_called_once_with('%Y%m%d%H%M%S')
    httputil.get_result.assert_called_once_with('setsystime.cgi', {'time': '20220611021555'})
