from unittest.mock import Mock, patch

from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.actions.setautoofftime import SetAutoOffTime
from m300_toolbox.http.http import Http


class TestSetAutoOffTime(absltest.TestCase):

  def test_timeTooShort_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetAutoOffTime.FLAG, '0')):
        pass

  def test_timeTooLong_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetAutoOffTime.FLAG, '2147483648')):
        pass

  @patch.object(Http, 'get', Mock())
  def test_goodTime_callsApi(self):
    SetAutoOffTime.execute(10)
    Http.get.assert_called_once_with('setparkingattr.cgi', {'entertime': 10})
