from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.files.filetype import FileType
from src.files.getfilecount import get_file_count

_GET_HTTP_RESPONSE_MAGIC_MOCK_1 = MagicMock(return_value=SimpleNamespace(
    text='{"ResultCode":"0","Result":['
    '{"type":"0","count":"100"},'
    '{"type":"1","count":"200"},'
    '{"type":"2","count":"300"},'
    '{"type":"3","count":"400"},'
    '{"type":"4","count":"500"},'
    '{"type":"5","count":"600"},'
    ']}'))

_GET_HTTP_RESPONSE_MAGIC_MOCK_2 = MagicMock(return_value=SimpleNamespace(
    text='{"ResultCode":"0","Result":['
    '{"type":"0","count":"100"},'
    '{"type":"1","count":"200"},'
    '{"type":"2","count":"300"},'
    '{"type":"3","count":"400"},'
    '{"type":"4","count":"500"},'
    ']}'))


class TestGetFileCount(TestCase):

  @patch('src.http.httputil._get_http_response', _GET_HTTP_RESPONSE_MAGIC_MOCK_1)
  def test_get_file_count(self) -> None:
    self.assertEqual(get_file_count(FileType.NORMAL), 100)
    self.assertEqual(get_file_count(FileType.PARKING), 300)
    self.assertEqual(get_file_count(FileType.TIME_LAPSE), 600)

  @patch('src.http.httputil._get_http_response', _GET_HTTP_RESPONSE_MAGIC_MOCK_2)
  def test_missing_file_count_raises_value_error(self) -> None:
    with self.assertRaises(ValueError):
      get_file_count(FileType.TIME_LAPSE)
