from unittest.mock import Mock, patch

from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.actions.setvideosplittime import SetVideoSplitTime
from m300_toolbox.http.http import Http


class TestSetVideoSplitTime(absltest.TestCase):

  def test_shortTime_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetVideoSplitTime.FLAG, '59')):
        pass

  def test_longTime_raises(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((SetVideoSplitTime.FLAG, '2136')):
        pass

  @flagsaver.as_parsed((SetVideoSplitTime.FLAG, '60'))
  @patch.object(Http, 'get', Mock())
  def test_goodTime_callsApi(self):
    SetVideoSplitTime.execute(60)
    Http.get.assert_called_once_with('setsplittime.cgi', {'splittime': 60})
