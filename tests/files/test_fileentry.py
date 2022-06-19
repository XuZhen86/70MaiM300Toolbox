from unittest import TestCase

from src.files.fileentry import FileEntry
from src.files.filetype import FileType


class TestFileEntry(TestCase):

  def test_parses_from_result(self):
    file_entry = FileEntry(
        {
            'path': 'sd/Lapse',
            'name': 'LA20211112-194823-000002.mp4',
            'size': '5373952',
            'type': '5'
        }, 5373952, FileType.TIME_LAPSE)

    self.assertEqual(file_entry.path, 'sd/Lapse')
    self.assertEqual(file_entry.name, 'LA20211112-194823-000002.mp4')
    self.assertEqual(file_entry.size_b, 5373952)
    self.assertEqual(file_entry.file_type, FileType.TIME_LAPSE)

  def test_ignores_result_size_field(self):
    file_entry = FileEntry(
        {
            'path': 'sd/Lapse',
            'name': 'LA20211112-194823-000002.mp4',
            'size': '5373952',
            'type': '5'
        }, 100, FileType.TIME_LAPSE)

    self.assertEqual(file_entry.size_b, 100)

  def test_ignores_result_type_field(self):
    file_entry = FileEntry(
        {
            'path': 'sd/Lapse',
            'name': 'LA20211112-194823-000002.mp4',
            'size': '5373952',
            'type': '5'
        }, 100, FileType.NORMAL)

    self.assertEqual(file_entry.file_type, FileType.NORMAL)

  def test_missing_key_raises_key_error(self):
    with self.assertRaises(KeyError):
      FileEntry({}, 100, FileType.NORMAL)

  def test_compare_based_on_timestamp_only(self):
    file_entry_1 = FileEntry({
        'path': 'sd/Parking',
        'name': 'PA20211112-194823-000003.mp4',
    }, 100, FileType.PARKING)
    file_entry_2 = FileEntry({
        'path': 'sd/Normal',
        'name': 'LA20211112-194824-000002.mp4',
    }, 100, FileType.NORMAL)

    self.assertLess(file_entry_1, file_entry_2)

  def test_compare_sequence_number_if_same_timestamp(self):
    file_entry_1 = FileEntry({
        'path': 'sd/Parking',
        'name': 'PA20211112-194823-000002.mp4',
    }, 100, FileType.PARKING)
    file_entry_2 = FileEntry({
        'path': 'sd/Normal',
        'name': 'LA20211112-194823-000003.mp4',
    }, 100, FileType.NORMAL)

    self.assertLess(file_entry_1, file_entry_2)

  def test_get_local_path_normal(self):
    file_entry = FileEntry({
        'path': 'sd/Normal',
        'name': 'NO20220610-121418-001120.mp4'
    }, 100, FileType.NORMAL)

    self.assertEqual(file_entry.get_local_path(), 'Normal/20220610/NO20220610-121418-001120.mp4')

  def test_get_local_path_parking(self):
    file_entry = FileEntry({
        'path': 'sd/Parking',
        'name': 'PA20211125-124504-000326.mp4'
    }, 100, FileType.PARKING)

    self.assertEqual(file_entry.get_local_path(), 'Parking/20211125/PA20211125-124504-000326.mp4')

  def test_get_local_path_time_lapse(self):
    file_entry = FileEntry({
        'path': 'sd/Lapse',
        'name': 'LA20220610-224543-001143.mp4'
    }, 100, FileType.TIME_LAPSE)

    self.assertEqual(file_entry.get_local_path(), 'TimeLapse/20220610/LA20220610-224543-001143.mp4')
