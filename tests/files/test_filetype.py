from unittest import TestCase

from src.files.filetype import FileType


class TestFileType(TestCase):

  def test(self) -> None:
    self.assertEqual(FileType(0).get_local_path(), 'Normal')

    with self.assertRaises(NotImplementedError):
      FileType(1).get_local_path()

    self.assertEqual(FileType(2).get_local_path(), 'Parking')

    with self.assertRaises(NotImplementedError):
      FileType(3).get_local_path()

    with self.assertRaises(NotImplementedError):
      FileType(4).get_local_path()

    self.assertEqual(FileType(5).get_local_path(), 'TimeLapse')
