from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.setchimeonboot import SetChimeOnBoot
from m300_toolbox.http.http import Http


class TestSetChimeOnBoot(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    SetChimeOnBoot.execute(True)
    Http.get.assert_called_once_with('setbootmusic.cgi', {'enable': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_disables(self):
    SetChimeOnBoot.execute(False)
    Http.get.assert_called_once_with('setbootmusic.cgi', {'enable': 0})
