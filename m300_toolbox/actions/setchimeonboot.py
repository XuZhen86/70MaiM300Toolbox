from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetChimeOnBoot(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_chime_on_boot',
      default=None,
      help='Sets if a chime is played when the dashcam is turned on. ',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setbootmusic.cgi', {'enable': int(enable)})
