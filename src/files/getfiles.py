import os

from absl import logging
from src.files import getfileentries
from src.files.filetype import FileType
from src.http import httputil


def get_files(file_type: FileType) -> None:
  file_entries = getfileentries.get_file_entries(file_type)
  file_entries.sort()

  for i, file_entry in enumerate(file_entries):
    path = file_entry.path
    name = file_entry.name
    size_b = file_entry.size_b

    local_path = file_entry.get_local_path()

    if os.path.exists(local_path) and os.path.getsize(local_path) == size_b:
      logging.info('(%s / %s) skip %s', i + 1, len(file_entries), name)
      continue
    logging.info('(%s / %s) downloading %s', i + 1, len(file_entries), name)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    # https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content
    content_iterator = httputil.get_content_iterator(f'http://192.168.0.1/{path}/{name}')
    with open(local_path, 'wb') as local_file:
      for chunk in content_iterator:
        local_file.write(chunk)
