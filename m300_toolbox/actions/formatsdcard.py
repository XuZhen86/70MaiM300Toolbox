from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class FormatSdCard(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='format_sd_card',
      default=None,
      help='Formats and clears SD card. '
      'The light ring will flash blue and recording will be paused during formatting. '
      'There\'s a chance that the formatting will fail and the light ring will turn red.',
  )

  @classmethod
  @override
  def execute(cls, do_formatting: bool) -> None:
    if do_formatting:
      Http.get('sdcommand.cgi', {'format': 1})
