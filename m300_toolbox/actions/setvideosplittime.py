from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetVideoSplitTime(Action[int, None]):
  FLAG = flags.DEFINE_integer(
      name='set_video_split_time',
      default=None,
      lower_bound=1 * 60,
      upper_bound=35 * 60 + 35,
      help='Sets the max length in seconds of the video files. '
      'The max video length is bounded by the max file size of the FAT32 file system. '
      'At 35:35, H264 1080p recording reaches the maximum 4GB file size. '
      'The API does not return accurate file sizes for >2GB files. '
      'Setting the value to less than 1020 (that is 17 minutes) is recommended.',
  )

  @classmethod
  @override
  def execute(cls, time_s: int) -> None:
    Http.get('setsplittime.cgi', {'splittime': time_s})
