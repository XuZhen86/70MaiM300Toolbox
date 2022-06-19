from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.files.filetype import FileType
from src.files.getfileentries import get_file_entries

_HTTPUTIL_GET_RESULT_VALUE = [
    {
        'path': 'sd/Normal',
        'name': 'NO20220610-121518-001121.mp4',
        'size': '20971520',
        'type': '0'
    },
    {
        'path': 'sd/Normal',
        'name': 'NO20220610-121418-001120.mp4',
        'size': '125829120',
        'type': '0'
    },
    {
        'path': 'sd/Normal',
        'name': 'NO20220610-121318-001119.mp4',
        'size': '125829120',
        'type': '0'
    },
]

_HTTP_HEADER_CONTENT_LENGTH = 12345678


class TestGetFileEntries(TestCase):

  @patch('src.files.getfilecount.get_file_count', MagicMock(return_value=0))
  def test_zero_file_count(self):
    file_entries = get_file_entries(FileType.NORMAL)
    self.assertEqual(file_entries, [])

  @patch('src.files.getfilecount.get_file_count',
         MagicMock(return_value=len(_HTTPUTIL_GET_RESULT_VALUE)))
  @patch('src.http.httputil.get_result', MagicMock(return_value=_HTTPUTIL_GET_RESULT_VALUE))
  @patch('src.http.httputil.get_http_headers',
         MagicMock(return_value={'Content-Length': str(_HTTP_HEADER_CONTENT_LENGTH)}))
  def test_non_zero_file_count(self):
    file_entries = get_file_entries(FileType.NORMAL)

    self.assertEqual(len(file_entries), len(_HTTPUTIL_GET_RESULT_VALUE))
    for i, file_entry in enumerate(file_entries):
      self.assertEqual(file_entry.path, _HTTPUTIL_GET_RESULT_VALUE[i]['path'])
      self.assertEqual(file_entry.name, _HTTPUTIL_GET_RESULT_VALUE[i]['name'])
      self.assertEqual(file_entry.size_b, _HTTP_HEADER_CONTENT_LENGTH)
      self.assertEqual(file_entry.file_type, FileType.NORMAL)
