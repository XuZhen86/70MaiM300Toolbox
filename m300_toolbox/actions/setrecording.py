from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetRecording(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_recording',
      default=None,
      help='Continue or pause the recording. '
      'The dashcam keeps recording while the data is being transferred, and the files may not stay static. '
      'It can be helpful to stop the recording during a data transfer to mitigate this issue. '
      'It also saves car battery when not recording and is helpful when the car is parked in a garage.',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setaccessalbum.cgi', {'enable': int(enable)})


# record.cgi doesn't work for M300.
# httputil.get_result('record.cgi', {'cmd': 'start' if is_recording else 'stop'})
