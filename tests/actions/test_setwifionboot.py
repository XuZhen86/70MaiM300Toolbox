from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.setwifionboot import SetWifiOnBoot
from m300_toolbox.http.http import Http


class TestWifiOnBoot(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetWifiOnBoot.execute(True)
    Http.get.assert_called_once_with('setwifiboot.cgi', {'enable': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetWifiOnBoot.execute(False)
    Http.get.assert_called_once_with('setwifiboot.cgi', {'enable': 0})
