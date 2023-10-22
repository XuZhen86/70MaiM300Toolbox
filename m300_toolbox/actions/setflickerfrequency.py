from enum import IntEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class FlickerFrequency(IntEnum):
  FREQ_60HZ = 0
  FREQ_55HZ = 2
  FREQ_50HZ = 1


class SetFlickerFrequency(Action[FlickerFrequency, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_flicker_frequency',
      default=None,
      enum_class=FlickerFrequency,
      help='Sets the local power line frequency for flicker resistance.',
  )

  @classmethod
  @override
  def execute(cls, frequency: FlickerFrequency) -> None:
    Http.get('setp1n0.cgi', {'ntscpal': int(frequency)})
