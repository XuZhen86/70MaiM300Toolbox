from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.setaudiorecording import SetAudioRecording
from m300_toolbox.http.http import Http


class TestSetAudioRecording(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetAudioRecording.execute(True)
    Http.get.assert_called_once_with('setaudioin.cgi', {'enable': 0})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetAudioRecording.execute(False)
    Http.get.assert_called_once_with('setaudioin.cgi', {'enable': 1})
