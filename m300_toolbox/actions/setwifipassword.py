from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetWifiPassword(Action[str, None]):
  FLAG = flags.DEFINE_string(
      name='set_wifi_password',
      default=None,
      help='Sets a new Wi-Fi password that\'s between 8 and 63 characters in length. '
      'Expect Wi-Fi to disconnect after setting the new password. '
      'You may not be able to change the Wi-Fi password from 70Mai app if the password is longer than 8 characters.',
  )

  @classmethod
  @override
  def execute(cls, password: str) -> None:
    Http.get('setwifi.cgi', {'wifikey': password})

  @staticmethod
  @override
  def flag_validator(password: str | None) -> bool:
    if password is None:
      return True

    if password is not None and not 8 <= len(password) <= 63:
      raise flags.ValidationError('Password length must be between 8 and 63. '
                                  f'Got {len(password)} instead.')

    return True
