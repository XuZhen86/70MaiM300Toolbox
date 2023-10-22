from typing import override

import jsonschema
from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class GetFileCounts(Action[bool, dict[int, int] | None]):
  FLAG = flags.DEFINE_boolean(
      name='get_file_count',
      default=None,
      help='Get the number of files under each file category.',
  )

  @classmethod
  @override
  def execute(cls, get_counts: bool) -> dict[int, int] | None:
    if not get_counts:
      return

    result = Http.get('getfilecount.cgi', {}, cls._text_response_fixer)
    cls.RESULT_VALIDATOR.validate(result)
    assert isinstance(result, list)

    return {int(item['type']): int(item['count']) for item in result}

  RESULT_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'array',
      'items': {
          'type': 'object',
          'required': ['type', 'count'],
          'properties': {
              'type': {
                  'type': 'string',
                  'pattern': r'^\d+$'
              },
              'count': {
                  'type': 'string',
                  'pattern': r'^\d+$'
              }
          }
      }
  })

  @staticmethod
  def _text_response_fixer(text: str) -> str:
    '''
      The response text has a trailing comma that breaks json.load().
      Example:
      {[
          {'type': '0', 'count': '122'},
          {'type': '1', 'count': '0'},
          {'type': '2', 'count': '11'},
          {'type': '3', 'count': '0'},
          {'type': '4', 'count': '0'},
          {'type': '5', 'count': '86'},  # Here
      ]}
    '''
    return text[:-3] + ']}'


jsonschema.Draft202012Validator.check_schema(GetFileCounts.RESULT_VALIDATOR.schema)
