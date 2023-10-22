from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.reset import Reset
from m300_toolbox.http.http import Http


class TestReset(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    Reset.execute(True)
    Http.get.assert_called_once_with('reset.cgi')

  @patch.object(Http, 'get', Mock())
  def test_false_doNothing(self):
    Reset.execute(False)
    Http.get.assert_not_called()
