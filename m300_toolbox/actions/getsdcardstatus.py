from dataclasses import dataclass
from typing import override

import jsonschema
from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@dataclass(frozen=True)
class SdCardStatus:
  state: str
  capacity_mb: int
  used_mb: int  # Does not include the file that's being actively written to.

  def __str__(self) -> str:
    lines = [
        'SdCardStatus:',
        f'  State: {self.state}',
        f'  Capacity: {self.capacity_mb} MB',
    ]

    if self.capacity_mb == 0:
      lines.append(f'  Used: {self.used_mb} MB')
    else:
      lines.append(f'  Used: {self.used_mb} MB, {int(self.used_mb / self.capacity_mb * 100)}%')

    return '\n'.join(lines)


class GetSdCardStatus(Action[bool, SdCardStatus | None]):
  FLAG = flags.DEFINE_boolean(
      name='get_sd_card_status',
      default=None,
      help='Reads and prints SD card status. '
      'The status includes the state, total capacity in MB, and used capacity in MB. '
      'The used capacity does not include the file that is being actively written to.',
  )

  RESULT_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'object',
      'required': ['sdstate', 'sdtotal', 'sdused'],
      'properties': {
          'sdstate': {
              'type': 'string'
          },
          'sdtotal': {
              'type': 'string',
              'pattern': r'^\d+MB$'
          },
          'sdused': {
              'type': 'string',
              'pattern': r'^\d+MB$'
          }
      }
  })

  @classmethod
  @override
  def execute(cls, b: bool) -> SdCardStatus | None:
    if not b:
      return

    result = Http.get('getsdstate.cgi')
    cls.RESULT_VALIDATOR.validate(result)
    assert isinstance(result, dict)

    return SdCardStatus(
        state=str(result['sdstate']),
        capacity_mb=int(result['sdtotal'][:-2]),
        used_mb=int(result['sdused'][:-2]),
    )


jsonschema.Draft202012Validator.check_schema(GetSdCardStatus.RESULT_VALIDATOR.schema)
