from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetVoiceControl(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_voice_control',
      default=None,
      help='Enable or disable voice control.',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setvoicecontrol.cgi', {'enable': int(enable)})
