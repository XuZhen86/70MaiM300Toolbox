import time
from unittest.mock import Mock, patch

from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.actions.settimestamp import SetTimestamp
from m300_toolbox.http.http import Http


class TestSetTimestamp(absltest.TestCase):

  def test_invalidTimestamp_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetTimestamp.FLAG, '00001021223634')):
        pass

  @patch.object(Http, 'get', Mock())
  def test_validTimestamp_callsApi(self):
    SetTimestamp.execute('20231021223634')
    Http.get.assert_called_once_with('setsystime.cgi', {'time': '20231021223634'})

  @patch.object(time, 'strftime', Mock(return_value='20231021223634'))
  @patch.object(time, 'strptime', Mock())  # It calls strftime() under the hood.
  @patch.object(Http, 'get', Mock())
  def test_autoGenerateTimestamp_callsApi(self):
    SetTimestamp.execute('-')
    Http.get.assert_called_once_with('setsystime.cgi', {'time': '20231021223634'})
    time.strftime.assert_called_once_with('%Y%m%d%H%M%S')
