import os

from absl import logging
from src.files import getfileentries
from src.files.filetype import FileType
from src.http import httputil


def purge_files(file_type: FileType) -> None:
  file_entries = getfileentries.get_file_entries(file_type)
  file_entries.sort()

  for i, file_entry in enumerate(file_entries):
    path = file_entry.path
    name = file_entry.name
    size_b = file_entry.size_b

    local_path = file_entry.get_local_path()

    if not os.path.exists(local_path) or os.path.getsize(local_path) != size_b:
      logging.info('(%s / %s) skip %s', i + 1, len(file_entries), name)
      continue
    logging.info('(%s / %s) deleting %s', i + 1, len(file_entries), name)

    httputil.get_result('delete.cgi', {'path': path, 'name': name})
