from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetAudioRecording(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_audio_recording',
      default=None,
      help='Sets if audio is recorded with the video. ',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setaudioin.cgi', {'enable': int(not enable)})  # The value is flipped.
