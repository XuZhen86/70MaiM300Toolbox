from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetTimeLapseRecording(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_time_lapse_recording',
      default=None,
      help='Turn the time lapse recording on or off. '
      'The dashcam can continue to record time lapse videos when the vehicle is parked. '
      '1 frame is captured each second and the outputted video is in 30fps.'
      'The parking wire needs to be detected before entering time lapse recording.',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setlapserecattr.cgi', {'enable': int(enable)})
