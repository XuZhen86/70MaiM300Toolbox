import os
import tempfile
from unittest.mock import Mock, call, patch

from absl.testing import absltest, flagsaver

from m300_toolbox.actions.getfilecounts import GetFileCounts
from m300_toolbox.actions.getfileentries import FileEntry, GetFileEntries
from m300_toolbox.actions.getfiles import GetFiles
from m300_toolbox.http.http import Http


class TestGetFiles(absltest.TestCase):

  def setUp(self):
    self.previous_work_dir = os.getcwd()
    self.temp_dir = tempfile.TemporaryDirectory()
    os.chdir(self.temp_dir.name)
    return super().setUp()

  def tearDown(self) -> None:
    os.chdir(self.previous_work_dir)
    self.temp_dir.cleanup()
    return super().tearDown()

  @patch.object(GetFileCounts, 'execute', Mock())
  @patch.object(GetFileEntries, 'execute2', Mock())
  def test_false_doNothing(self):
    GetFiles.execute(False)
    GetFileCounts.execute.assert_not_called()
    GetFileEntries.execute2.assert_not_called()

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 0, 1: 0}))
  @patch.object(GetFileEntries, 'execute2', Mock())
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0']))
  def test_fileTypeDirsLengthMismatch_raises(self):
    with self.assertRaises(ValueError):
      GetFiles.execute(True)
    GetFileCounts.execute.assert_called_once_with(True)
    GetFileEntries.execute2.assert_not_called()

    self.assertRaisesWithLiteralMatch

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 0, 1: 0}))
  @patch.object(GetFileEntries, 'execute2', Mock(side_effect=[iter([]), iter([])]))
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0', 'file_type_dir_1']))
  def test_multipleFileTypes_iteratesAll(self):
    GetFiles.execute(True)
    GetFileCounts.execute.assert_called_once_with(True)
    GetFileEntries.execute2.assert_has_calls([call(0, 0), call(1, 0)])

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 1}))
  @patch.object(
      GetFileEntries, 'execute2',
      Mock(return_value=iter([
          FileEntry(path='sd/Normal',
                    name='NO20220610-121518-001121.mp4',
                    size_b=4,
                    content_length_b=4,
                    type=0)
      ])))
  @patch.object(Http, 'content', Mock(return_value=b'4444'))
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0']))
  @flagsaver.as_parsed((GetFiles.PURGE_AFTER_DOWNLOAD, 'false'))
  def test_noExistingFiles_createsFiles(self):
    local_dir = os.path.join(self.temp_dir.name, 'file_type_dir_0', '20220610')
    local_path = os.path.join(local_dir, 'NO20220610-121518-001121.mp4')

    GetFiles.execute(True)

    GetFileCounts.execute.assert_called_once_with(True)
    GetFileEntries.execute2.assert_called_once_with(0, 1)
    Http.content.assert_called_once_with(
        'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4')
    with open(local_path, 'rb') as local_file:
      content = local_file.read()
      self.assertEqual(content, b'4444')

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 1}))
  @patch.object(
      GetFileEntries, 'execute2',
      Mock(return_value=iter([
          FileEntry(path='sd/Normal',
                    name='NO20220610-121518-001121.mp4',
                    size_b=4,
                    content_length_b=4,
                    type=0)
      ])))
  @patch.object(Http, 'content', Mock(return_value=b'4444'))
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0']))
  @flagsaver.as_parsed((GetFiles.PURGE_AFTER_DOWNLOAD, 'false'))
  def test_existingFileDifferentSize_overwritesFile(self):
    local_dir = os.path.join(self.temp_dir.name, 'file_type_dir_0', '20220610')
    local_path = os.path.join(local_dir, 'NO20220610-121518-001121.mp4')
    os.makedirs(local_dir)
    with open(local_path, 'wb') as local_file:
      local_file.write(b'22')

    GetFiles.execute(True)

    GetFileCounts.execute.assert_called_once_with(True)
    GetFileEntries.execute2.assert_called_once_with(0, 1)
    Http.content.assert_called_once_with(
        'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4')
    with open(local_path, 'rb') as local_file:
      content = local_file.read()
      self.assertEqual(content, b'4444')

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 1}))
  @patch.object(
      GetFileEntries, 'execute2',
      Mock(return_value=iter([
          FileEntry(path='sd/Normal',
                    name='NO20220610-121518-001121.mp4',
                    size_b=4,
                    content_length_b=4,
                    type=0)
      ])))
  @patch.object(Http, 'content', Mock(return_value=b'4444'))
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0']))
  @flagsaver.as_parsed((GetFiles.PURGE_AFTER_DOWNLOAD, 'false'))
  def test_existingFileSameSize_skippsFile(self):
    local_dir = os.path.join(self.temp_dir.name, 'file_type_dir_0', '20220610')
    local_path = os.path.join(local_dir, 'NO20220610-121518-001121.mp4')
    os.makedirs(local_dir)
    with open(local_path, 'wb') as local_file:
      local_file.write(b'4444')

    GetFiles.execute(True)

    GetFileCounts.execute.assert_called_once_with(True)
    GetFileEntries.execute2.assert_called_once_with(0, 1)
    Http.content.assert_not_called()
    with open(local_path, 'rb') as local_file:
      content = local_file.read()
      self.assertEqual(content, b'4444')

  @patch.object(GetFileCounts, 'execute', Mock(return_value={0: 1}))
  @patch.object(
      GetFileEntries, 'execute2',
      Mock(return_value=iter([
          FileEntry(path='sd/Normal',
                    name='NO20220610-121518-001121.mp4',
                    size_b=4,
                    content_length_b=4,
                    type=0)
      ])))
  @patch.object(Http, 'content', Mock(return_value=b'4444'))
  @patch.object(Http, 'get', Mock())
  @flagsaver.as_parsed((GetFiles.FILE_TYPE_DIRS, ['file_type_dir_0']))
  @flagsaver.as_parsed((GetFiles.PURGE_AFTER_DOWNLOAD, 'true'))
  def test_purgeAfterDownload_fileDeleted(self):
    GetFiles.execute(True)

    Http.get.assert_called_once_with('delete.cgi', {
        'path': 'sd/Normal',
        'name': 'NO20220610-121518-001121.mp4'
    })

  # The current implementation reads the entire file into the memory before writing it to disk.
  # Assuming this is fine for now.
  def test_bigFile(self):
    pass
