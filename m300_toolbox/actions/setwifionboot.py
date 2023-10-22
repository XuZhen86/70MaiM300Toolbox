from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetWifiOnBoot(Action[bool, None]):
  FLAG = flags.DEFINE_boolean(
      name='set_wifi_on_boot',
      default=None,
      help='Sets if Wi-Fi is enabled when the dashcam is turned on. '
      'Wi-Fi can stay enabled when the dashcam is in normal and is in time-lapse mode. '
      'Wi-Fi is always disabled when the dashcam is off or is in parking mode.',
  )

  @classmethod
  @override
  def execute(cls, enable: bool) -> None:
    Http.get('setwifiboot.cgi', {'enable': int(enable)})
