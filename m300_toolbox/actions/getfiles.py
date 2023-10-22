import os
from typing import override

from absl import flags, logging

from m300_toolbox.actions.action import Action
from m300_toolbox.actions.getfilecounts import GetFileCounts
from m300_toolbox.actions.getfileentries import GetFileEntries
from m300_toolbox.http import Http


class GetFiles(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='get_files',
      default=None,
      help='Downloads and organizes files to local storage. '
      'Files with matching names and sizes are skipped. '
      'Files are organized into directory structure like: $PWD/<type_dir>/YYYYMMDD/file_name.',
  )

  FILE_TYPE_DIRS = flags.DEFINE_multi_string(
      name='file_type_dirs',
      default=['Normal', 'Unknown1', 'Parking', 'Unknown3', 'Unknown4', 'TimeLapse'],
      help='Sets the directories to put each type of video files into.',
  )

  PURGE_AFTER_DOWNLOAD = flags.DEFINE_boolean(
      name='purge_after_download',
      default=False,
      help='Sets if files are deleted from the dashcam after they are successfully downloaded. '
      'Files are deleted if there are local files with matching name and size.',
  )

  @classmethod
  @override
  def execute(cls, b: bool) -> None:
    if not b:
      return

    file_counts = GetFileCounts.execute(True)
    assert file_counts is not None
    if len(file_counts) != len(cls.FILE_TYPE_DIRS.value):
      e = ValueError(f'Expected {len(file_counts)} values for --file_type_dirs, '
                     f'got {len(cls.FILE_TYPE_DIRS.value)} instead.')
      e.add_note(f'{file_counts=}')
      raise e

    for file_type, count in file_counts.items():
      file_type_dir = cls.FILE_TYPE_DIRS.value[file_type]

      for file_entry in GetFileEntries.execute2(file_type, count):
        path = file_entry.path
        name = file_entry.name
        local_path = os.path.join(file_type_dir, name[2:-18], name)

        if file_entry.content_length_b is not None:
          size_b = file_entry.content_length_b
        else:  # Fall back to using inaccurate size.
          size_b = file_entry.size_b
          logging.warning(
              f'True file size for {name} is unavailable, falling back to estimated size. '
              'The file may be downloaded repeatedly due to the inaccurate estimated size.')

        if not os.path.exists(local_path) or os.path.getsize(local_path) != size_b:
          os.makedirs(os.path.dirname(local_path), exist_ok=True)
          with open(local_path, 'wb') as local_file:
            local_file.write(Http.content(f'http://192.168.0.1/{path}/{name}'))

        if cls.PURGE_AFTER_DOWNLOAD.value:
          Http.get('delete.cgi', {'path': path, 'name': name})
