import datetime
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from m300_toolbox.http import httputil
from m300_toolbox.misc import synctime


@patch('datetime.datetime',
       SimpleNamespace(now=MagicMock(return_value=SimpleNamespace(strftime=MagicMock(
           return_value='20220611021555')))))
@patch('m300_toolbox.http.httputil.get_result', MagicMock(return_value=None))
@patch('builtins.print', MagicMock(return_value=None))
class TestSyncTime(TestCase):

  def test(self) -> None:
    synctime.sync_time()

    datetime.datetime.now().strftime.assert_called_once_with('%Y%m%d%H%M%S')
    httputil.get_result.assert_called_once_with('setsystime.cgi', {'time': '20220611021555'})
    print.assert_called_once_with('synced to time: 20220611021555')
