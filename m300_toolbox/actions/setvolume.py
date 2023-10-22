from enum import IntEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class Volume(IntEnum):
  HIGH = 0
  MID = 1
  LOW = 2
  MUTE = 3


class SetVolume(Action[Volume, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_volume',
      default=None,
      enum_class=Volume,
      help='Sets the speaker volume. '
      'Mute disables all sound output and the only indicator of dashcam operation is the light ring.',
  )

  @classmethod
  @override
  def execute(cls, volume: Volume) -> None:
    Http.get('setaudiooutvolume.cgi', {'level': int(volume)})
