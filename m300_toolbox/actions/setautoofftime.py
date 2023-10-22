from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetAutoOffTime(Action[int, None]):
  FLAG = flags.DEFINE_integer(
      name='set_auto_off_time',
      default=None,
      lower_bound=1,  # Setting it to 0 causes the dashcam to shutdown immediately after booting up.
      upper_bound=2147483647,
      help='Sets the time in minutes before turning off if the vehicle stays stationary. '
      'It is helpful when the dashcam is wired to a power supply that does not turn off when the car is off. '
      'Once automatically turned off, the dashcam must be manually turned on by clicking the power button. '
      'Setting the value to 0 causes the dashcam to turn off immediately after booting up. '
      'If this happens, click the reset button to turn it on, then click the reset button immediately when the blue light turns off. '
      'It may take a few tries to get it to work.',
  )

  @classmethod
  @override
  def execute(cls, time_m: int) -> None:
    Http.get('setparkingattr.cgi', {'entertime': time_m})
