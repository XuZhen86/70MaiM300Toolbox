from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.setvoicecontrol import SetVoiceControl
from m300_toolbox.http.http import Http


class TestSetVoiceControl(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetVoiceControl.execute(True)
    Http.get.assert_called_once_with('setvoicecontrol.cgi', {'enable': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetVoiceControl.execute(False)
    Http.get.assert_called_once_with('setvoicecontrol.cgi', {'enable': 0})
