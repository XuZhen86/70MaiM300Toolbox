import os
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from src.files import purgefiles
from src.files.fileentry import FileEntry
from src.files.filetype import FileType
from src.http import httputil

_CHUNK_SIZE = 420**2
_CHUNK_COUNT = 3

_FILE_ENTRIES = [
    FileEntry({
        'path': 'sd/Normal',
        'name': 'NO20220610-121518-001121.mp4'
    }, _CHUNK_SIZE * _CHUNK_COUNT, FileType.NORMAL),
    FileEntry({
        'path': 'sd/Normal',
        'name': 'NO20220609-121418-001120.mp4'
    }, _CHUNK_SIZE * _CHUNK_COUNT, FileType.NORMAL),
    FileEntry({
        'path': 'sd/Normal',
        'name': 'NO20220610-121318-001119.mp4'
    }, _CHUNK_SIZE * _CHUNK_COUNT, FileType.NORMAL),
]


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_result', MagicMock(return_value=None))
class TestLocalFilesDoNotExist(TestCase):

  def setUp(self) -> None:
    self.prev_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()
    os.chdir(self.temp_dir.name)

  def tearDown(self) -> None:
    os.chdir(self.prev_work_dir)
    self.temp_dir.cleanup()

  def test(self) -> None:
    purgefiles.purge_files(FileType.NORMAL)

    httputil.get_result.assert_not_called()


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_result', MagicMock(return_value=None))
class TestLocalFilesDifferentSizes(TestCase):

  def setUp(self) -> None:
    self.prev_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()

    for file_entry in _FILE_ENTRIES:
      abs_local_path = os.path.join(self.temp_dir.name, file_entry.get_local_path())
      os.makedirs(os.path.dirname(abs_local_path), exist_ok=True)
      with open(abs_local_path, 'wb') as local_file:
        local_file.write(b'\x00' * (file_entry.size_b - 1))

    os.chdir(self.temp_dir.name)

  def tearDown(self) -> None:
    os.chdir(self.prev_work_dir)
    self.temp_dir.cleanup()

  def test(self) -> None:
    purgefiles.purge_files(FileType.NORMAL)

    httputil.get_result.assert_not_called()


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_result', MagicMock(return_value=None))
class TestLocalFilesExist(TestCase):

  def setUp(self) -> None:
    self.prev_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()

    for file_entry in _FILE_ENTRIES:
      abs_local_path = os.path.join(self.temp_dir.name, file_entry.get_local_path())
      os.makedirs(os.path.dirname(abs_local_path), exist_ok=True)
      with open(abs_local_path, 'wb') as local_file:
        local_file.write(b'\x00' * file_entry.size_b)

    os.chdir(self.temp_dir.name)

  def tearDown(self) -> None:
    os.chdir(self.prev_work_dir)
    self.temp_dir.cleanup()

  def test(self) -> None:
    purgefiles.purge_files(FileType.NORMAL)

    self.assertEqual(httputil.get_result.call_count, len(_FILE_ENTRIES))
    httputil.get_result.assert_has_calls([
        call('delete.cgi', {
            'path': file_entry.path,
            'name': file_entry.name
        }) for file_entry in _FILE_ENTRIES
    ])
