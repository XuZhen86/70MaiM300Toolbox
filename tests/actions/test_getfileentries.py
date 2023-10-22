from unittest.mock import Mock, call, patch

from absl.testing import absltest
from jsonschema import ValidationError
from requests.models import CaseInsensitiveDict

from m300_toolbox.actions.getfilecounts import GetFileCounts
from m300_toolbox.actions.getfileentries import FileEntry, GetFileEntries
from m300_toolbox.http.http import Http


class TestGetFileEntries(absltest.TestCase):

  FILE_COUNTS = {0: 3, 1: 1}
  FILE_LIST = [{
      'path': 'sd/Normal',
      'name': 'NO20220610-121318-001119.mp4',
      'size': '-125829120',
      'type': '2'
  }, {
      'path': 'sd/Normal',
      'name': 'NO20220610-121418-001120.mp4',
      'size': '125829120',
      'type': '2'
  }, {
      'path': 'sd/Normal',
      'name': 'NO20220610-121518-001121.mp4',
      'size': '20971520',
      'type': '2'
  }]
  HTTP_HEADERS = [
      ValueError(),
      CaseInsensitiveDict({'Content-Length': 666_666}),
      CaseInsensitiveDict({'Content-Length': 777_777})
  ]
  HTTP_HEADERS_CALLS = [
      call('http://192.168.0.1/sd/Normal/NO20220610-121318-001119.mp4'),
      call('http://192.168.0.1/sd/Normal/NO20220610-121418-001120.mp4'),
      call('http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4')
  ]
  FILE_ENTRIES = [
      FileEntry(path='sd/Normal',
                name='NO20220610-121318-001119.mp4',
                size_b=4_169_138_176,
                content_length_b=None,
                type=0),
      FileEntry(path='sd/Normal',
                name='NO20220610-121418-001120.mp4',
                size_b=125_829_120,
                content_length_b=666_666,
                type=0),
      FileEntry(path='sd/Normal',
                name='NO20220610-121518-001121.mp4',
                size_b=20_971_520,
                content_length_b=777_777,
                type=0)
  ]

  @patch.object(GetFileCounts, 'execute', Mock(return_value=FILE_COUNTS))
  @patch.object(Http, 'get', Mock(return_value=FILE_LIST))
  @patch.object(Http, 'headers', Mock(side_effect=HTTP_HEADERS))
  def test_fileTypeExists_returnsFileEntries(self):
    file_entries = GetFileEntries.execute(0)
    self.assertListEqual(file_entries, self.FILE_ENTRIES)
    GetFileCounts.execute.assert_called_once_with(True)
    Http.get.assert_called_once_with('getfilelist.cgi', {'start': '1', 'end': 3, 'type': 0})
    Http.headers.assert_has_calls(self.HTTP_HEADERS_CALLS)

  @patch.object(GetFileCounts, 'execute', Mock(return_value=FILE_COUNTS))
  def test_fileTypeDoesNotExist_raises(self):
    with self.assertRaises(KeyError):
      GetFileEntries.execute(2)
    GetFileCounts.execute.assert_called_once_with(True)

  INVALID_FILE_LIST = [{
      'not_path': 'sd/Normal',
      'name': 'NO20220610-121518-001121.mp4',
  }]

  @patch.object(GetFileCounts, 'execute', Mock(return_value=FILE_COUNTS))
  @patch.object(Http, 'get', Mock(return_value=INVALID_FILE_LIST))
  def test_invalidFileList_raises(self):
    with self.assertRaises(ValidationError):
      GetFileEntries.execute(1)
    GetFileCounts.execute.assert_called_once_with(True)
    Http.get.assert_called_once_with('getfilelist.cgi', {'start': '1', 'end': 1, 'type': 1})
