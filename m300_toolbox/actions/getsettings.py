from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class GetSettings(Action[bool, dict | None]):
  FLAG = flags.DEFINE_boolean(
      name='get_settings',
      default=None,
      help='Reads all settings.',
  )

  @classmethod
  @override
  def execute(cls, b: bool) -> dict | None:
    if not b:
      return

    result = {
        'getAllMenu.cgi': Http.get('getAllMenu.cgi'),
        'getwifi.cgi': Http.get('getwifi.cgi'),
        'getdeviceattr.cgi': Http.get('getdeviceattr.cgi'),
        'getvoicecontrol.cgi': Http.get('getvoicecontrol.cgi'),

        # Output included in getAllMenu.cgi.
        # {'lapserec_on': '0'}
        # 'getlapserecattr.cgi': Http.get('getlapserecattr.cgi'),

        # Output included in getdeviceattr.cgi.
        # {'systime': '20230720183515'}
        # 'getsystime.cgi': Http.get('getsystime.cgi'),

        # Output included in getAllMenu.cgi.
        # {'Parking_entertime': '0', 'Parking_threshold': '0'}
        # 'getparkingattr.cgi': Http.get('getparkingattr.cgi'),
    }
    return result
