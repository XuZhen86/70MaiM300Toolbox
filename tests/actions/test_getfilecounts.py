from unittest.mock import Mock, patch

from absl.testing import absltest
from jsonschema import ValidationError

from m300_toolbox.actions.getfilecounts import GetFileCounts
from m300_toolbox.http.http import Http


class TestGetFileCounts(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_false_doNothing(self):
    GetFileCounts.execute(False)
    Http.get.assert_not_called()

  @patch.object(Http, 'get', Mock(return_value=[]))
  def test_emptyResult_returnsEmpty(self):
    file_counts = GetFileCounts.execute(True)
    self.assertDictEqual(file_counts, {})

  INVALID_RESULT = [{'type': 1, 'count': '1'}]

  @patch.object(Http, 'get', Mock(return_value=INVALID_RESULT))
  def test_invalidResult_raises(self):
    with self.assertRaises(ValidationError):
      GetFileCounts.execute(True)
    Http.get.assert_called_once_with('getfilecount.cgi', {}, GetFileCounts._text_response_fixer)

  NON_EMPTY_RESULT = [{'type': '1', 'count': '1'}, {'type': '2', 'count': '2'}]

  @patch.object(Http, 'get', Mock(return_value=NON_EMPTY_RESULT))
  def test_nonEmptyResult_returnsNonEmpty(self):
    file_counts = GetFileCounts.execute(True)
    self.assertDictEqual(file_counts, {1: 1, 2: 2})
    Http.get.assert_called_once_with('getfilecount.cgi', {}, GetFileCounts._text_response_fixer)
