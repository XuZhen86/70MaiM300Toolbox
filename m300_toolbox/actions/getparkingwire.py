from typing import override

import jsonschema
from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class GetParkingWire(Action[bool, bool | None]):
  FLAG = flags.DEFINE_boolean(
      name='get_parking_wire',
      default=None,
      help='Query if a parking wire is detected.',
  )

  RESULT_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'object',
      'required': ['parkingwire'],
      'properties': {
          'parkingwire': {
              'type': 'string',
              'pattern': r'^[01]$'
          }
      }
  })

  @classmethod
  @override
  def execute(cls, get: bool) -> bool | None:
    if not get:
      return None

    result = Http.get('getparkingwire.cgi')
    cls.RESULT_VALIDATOR.validate(result)
    assert isinstance(result, dict)

    return bool(result['parkingwire'])


jsonschema.Draft202012Validator.check_schema(GetParkingWire.RESULT_VALIDATOR.schema)
