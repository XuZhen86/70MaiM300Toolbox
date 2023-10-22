from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.settimelapserecording import SetTimeLapseRecording
from m300_toolbox.http.http import Http


class TestSetTimeLapseRecording(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetTimeLapseRecording.execute(True)
    Http.get.assert_called_once_with('setlapserecattr.cgi', {'enable': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetTimeLapseRecording.execute(False)
    Http.get.assert_called_once_with('setlapserecattr.cgi', {'enable': 0})
