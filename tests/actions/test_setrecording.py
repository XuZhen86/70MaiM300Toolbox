from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.setrecording import SetRecording
from m300_toolbox.http.http import Http


class TestSetRecording(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetRecording.execute(True)
    Http.get.assert_called_once_with('setaccessalbum.cgi', {'enable': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetRecording.execute(False)
    Http.get.assert_called_once_with('setaccessalbum.cgi', {'enable': 0})
