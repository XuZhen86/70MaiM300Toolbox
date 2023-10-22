from unittest.mock import Mock, patch

from absl.testing import absltest

from m300_toolbox.actions.formatsdcard import FormatSdCard
from m300_toolbox.http.http import Http


class TestFormatSdCard(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_true_enables(self):
    FormatSdCard.execute(True)
    Http.get.assert_called_once_with('sdcommand.cgi', {'format': 1})

  @patch.object(Http, 'get', Mock())
  def test_false_doNothing(self):
    FormatSdCard.execute(False)
    Http.get.assert_not_called()
