import os
import tempfile
from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.files import getfiles
from src.files.fileentry import FileEntry
from src.files.filetype import FileType

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

_GET_CONTENT_ITERATOR_MAGIC_MOCK = MagicMock(
    side_effect=lambda _: iter([b'\x00' * _CHUNK_SIZE] * _CHUNK_COUNT))


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_content_iterator', _GET_CONTENT_ITERATOR_MAGIC_MOCK)
class TestNoExistingFiles(TestCase):

  def setUp(self):
    self.prev_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()
    os.chdir(self.temp_dir.name)

  def tearDown(self):
    os.chdir(self.prev_work_dir)
    self.temp_dir.cleanup()

  def test(self):
    getfiles.get_files(FileType.NORMAL)

    for file_entry in _FILE_ENTRIES:
      abs_local_path = os.path.join(self.temp_dir.name, file_entry.get_local_path())
      self.assertTrue(os.path.exists(abs_local_path))
      self.assertEqual(os.path.getsize(abs_local_path), file_entry.size_b)


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_content_iterator', _GET_CONTENT_ITERATOR_MAGIC_MOCK)
class TestPartialExistingFiles(TestCase):

  def setUp(self):
    self.prev_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()

    abs_local_path = os.path.join(self.temp_dir.name, _FILE_ENTRIES[0].get_local_path())
    os.makedirs(os.path.dirname(abs_local_path))
    with open(abs_local_path, 'wb') as local_file:
      local_file.write(b'\x00' * (_FILE_ENTRIES[0].size_b // 3))

    os.chdir(self.temp_dir.name)

  def tearDown(self) -> None:
    os.chdir(self.prev_work_dir)
    self.temp_dir.cleanup()

  def test(self):
    getfiles.get_files(FileType.NORMAL)

    for file_entry in _FILE_ENTRIES:
      abs_local_path = os.path.join(self.temp_dir.name, file_entry.get_local_path())
      self.assertTrue(os.path.exists(abs_local_path))
      self.assertEqual(os.path.getsize(abs_local_path), file_entry.size_b)


@patch('src.files.getfileentries.get_file_entries', MagicMock(return_value=_FILE_ENTRIES))
@patch('src.http.httputil.get_content_iterator', _GET_CONTENT_ITERATOR_MAGIC_MOCK)
class TestFullExistingFiles(TestCase):

  def setUp(self):
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

  def test(self):
    getfiles.get_files(FileType.NORMAL)

    for file_entry in _FILE_ENTRIES:
      abs_local_path = os.path.join(self.temp_dir.name, file_entry.get_local_path())
      self.assertTrue(os.path.exists(abs_local_path))
      self.assertEqual(os.path.getsize(abs_local_path), file_entry.size_b)
