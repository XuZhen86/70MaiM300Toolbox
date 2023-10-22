import json
from typing import override

import jsonschema
from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SendCommandWithParams(Action[str, dict | list | None]):
  FLAG = flags.DEFINE_string(
      name='send_command',
      default=None,
      help='Manually send a command, useful for debugging. '
      '-timestamp and -signkey will be added automatically. '
      'The text payload will be printed.',
  )

  WITH_PARAMS = flags.DEFINE_string(
      name='with_params',
      default='{}',
      help='The optional params to be sent with the command. '
      'Must be a JSON-formatted object that can be decoded into type "dict[str, str | int]". '
      'This flag is ignored unless --send_command is set.',
  )

  PARAMS_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'object',
      'patternProperties': {
          '': {  # r'^.+$' also works.
              'type': ['string', 'integer']
          }
      }
  })

  @classmethod
  @override
  def execute(cls, command: str) -> dict | list | None:
    raw_params = json.loads(cls.WITH_PARAMS.value)
    cls.PARAMS_VALIDATOR.validate(raw_params)
    return Http.get(command, raw_params)


jsonschema.Draft202012Validator.check_schema(SendCommandWithParams.PARAMS_VALIDATOR.schema)
