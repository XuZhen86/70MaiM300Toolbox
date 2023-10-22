from unittest.mock import Mock, patch

from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.actions.setwifipassword import SetWifiPassword
from m300_toolbox.http.http import Http


class TestSetWifiPassword(absltest.TestCase):

  def test_shortPassword_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetWifiPassword.FLAG, '0' * 7)):
        pass

  def test_longPassword_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetWifiPassword.FLAG, '0' * 64)):
        pass

  @patch.object(Http, 'get', Mock())
  def test_goodPassword_callsApi(self):
    SetWifiPassword.execute('0' * 63)
    Http.get.assert_called_once_with('setwifi.cgi', {'wifikey': '0' * 63})
