from enum import StrEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class VideoCodec(StrEnum):
  H264 = 'h264'
  HEVC = 'hevc'


class SetVideoCodec(Action[VideoCodec, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_video_codec',
      default=None,
      enum_class=VideoCodec,
      help='Sets the video codec.',
  )

  @classmethod
  @override
  def execute(cls, codec: VideoCodec) -> None:
    Http.get('setparameter.cgi', {'workmode': 0, 'type': 0, 'videoencode': str(codec)})
