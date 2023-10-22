from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class Reset(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='reset',
      default=None,
      help='Resets the dashcam to factory default settings. '
      'Wi-Fi password would resets to "12345678" and it would require generating a new token.',
  )

  @classmethod
  @override
  def execute(cls, reset: bool) -> None:
    if reset:
      Http.get('reset.cgi')
