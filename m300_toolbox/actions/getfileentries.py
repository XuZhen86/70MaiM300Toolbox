from dataclasses import dataclass
from typing import Generator, override

import jsonschema
from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.actions.getfilecounts import GetFileCounts
from m300_toolbox.http import Http


@dataclass(frozen=True)
class FileEntry:
  path: str
  name: str
  type: int

  # Appears to always be rounded to 65536.
  # Roughly equals to the true file size.
  size_b: int

  # Equals to the true file fize.
  # Unavailable when the file is larger than 2GiB.
  content_length_b: int | None


class GetFileEntries(Action[int, list[FileEntry]]):
  FLAG = flags.DEFINE_integer(
      name='get_file_entries',
      default=None,
      help='Get info of the files for a given file type number.',
  )

  @classmethod
  @override
  def execute(cls, file_type: int) -> list[FileEntry]:
    file_counts = GetFileCounts.execute(True)
    assert file_counts is not None

    try:
      file_count = file_counts[file_type]
    except KeyError as e:
      e.add_note(f'{file_counts=}')
      e.add_note(f'{file_type=}')
      raise

    return list(cls.execute2(file_type, file_count))

  RESULT_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'array',
      'items': {
          'type': 'object',
          'required': ['path', 'name', 'size'],
          '$comment': 'Property "type" is ignored.',
          'properties': {
              'path': {
                  'type': 'string'
              },
              'name': {
                  'type': 'string',
                  'pattern': r'^[A-Z]{2}\d{8}-\d{6}-\d{6}\.mp4$'
              },
              'size': {
                  'type': "string",
                  'pattern': r'^-?\d{1,10}$'
              }
          }
      }
  })

  @classmethod
  def execute2(cls, file_type: int, file_count: int) -> Generator[FileEntry, None, None]:
    params = {'start': '1', 'end': file_count, 'type': file_type}
    result = Http.get('getfilelist.cgi', params)
    cls.RESULT_VALIDATOR.validate(result)
    assert isinstance(result, list)
    result.sort(key=lambda row: row['name'])

    for row in result:
      assert isinstance(row, dict)
      path = str(row['path'])
      name = str(row['name'])
      size = int(row['size'])

      # Size is a 32 bit signed int and rolls over to negative values.
      if size <= 0:
        size += (4 * 1024**3)

      try:
        headers = Http.headers(f'http://192.168.0.1/{path}/{name}')
        content_length = headers.get('Content-Length')
        if content_length is not None:
          content_length = int(content_length)
      except:
        content_length = None

      yield FileEntry(
          path=path,
          name=name,
          size_b=size,
          content_length_b=content_length,
          type=file_type,
      )


jsonschema.Draft202012Validator.check_schema(GetFileEntries.RESULT_VALIDATOR.schema)
