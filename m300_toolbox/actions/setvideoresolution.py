from enum import StrEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class VideoResolution(StrEnum):
  RES_1920X1080P30 = '1920x1080P30'
  RES_2304X1296P30 = '2304x1296P30'


class SetVideoResolution(Action[VideoResolution, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_video_resolution',
      default=None,
      enum_class=VideoResolution,
      help='Sets the video resolution. ',
  )

  @classmethod
  @override
  def execute(cls, res: VideoResolution) -> None:
    Http.get('setparameter.cgi', {'workmode': 0, 'type': 0, 'value': str(res)})
