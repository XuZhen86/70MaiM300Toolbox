from absl import logging
from src.files.filetype import FileType
from src.http import httputil


def get_file_count(file_type: FileType) -> int:
  results = httputil.get_result('getfilecount.cgi', {}, _text_response_preprocessor)
  logging.debug('results = %s', results)

  for result in results:
    if int(result['type']) == file_type:
      return int(result['count'])

  raise ValueError(f'no matching result for {file_type}')


# Cleanup response text, it has a trailing comma that breaks json.load().
# Example:
# [
#     {'type': '0', 'count': '122'},
#     {'type': '1', 'count': '0'},
#     {'type': '2', 'count': '11'},
#     {'type': '3', 'count': '0'},
#     {'type': '4', 'count': '0'},
#     {'type': '5', 'count': '86'},  # Here
# ]
def _text_response_preprocessor(text: str) -> str:
  return text[:-3] + ']}'
