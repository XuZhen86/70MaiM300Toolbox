from absl import logging

from src.files import getfilecount
from src.files.fileentry import FileEntry
from src.files.filetype import FileType
from src.http import httputil


def get_file_entries(file_type: FileType) -> list[FileEntry]:
  file_count = getfilecount.get_file_count(file_type)
  if file_count == 0:
    return []

  results = httputil.get_result('getfilelist.cgi', {
      'start': 1,
      'end': file_count,
      'type': int(file_type)
  })

  file_entries: list[FileEntry] = []
  for result in results:
    path: str = result['path']
    name: str = result['name']

    # The size in results isn't always accurate and can cause a file to never be purged.
    # Using HTTP header to get the real file size.
    # https://stackoverflow.com/a/44299915
    http_headers = httputil.get_http_headers(f'http://192.168.0.1/{path}/{name}')
    content_length_b = int(http_headers['Content-Length'])

    file_entry = FileEntry(result, content_length_b, file_type)
    file_entries.append(file_entry)

  logging.debug('file_entries = %s', file_entries)
  return file_entries
