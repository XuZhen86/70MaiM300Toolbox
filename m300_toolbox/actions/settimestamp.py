import time
from typing import override

from absl import flags, logging

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class SetTimestamp(Action[str, None]):
  TIME_FORMAT = '%Y%m%d%H%M%S'
  AUTO_GENERATE_TIMESTAMP = '-'

  FLAG = flags.DEFINE_string(
      name='set_timestamp',
      default=None,
      help='Sets the current timestamp. '
      'The timestamp shown in the video will always equal to the timestamp set here. '
      'The dashcam does not have a concept of timezone, and the timestamp has to be updated when the timezone or Daylight Saving Time changes. '
      f'Supply a timestamp in the format of "{TIME_FORMAT}". Use $(date +\'{TIME_FORMAT}\') to generate the timestamp. '
      f'Supply "{AUTO_GENERATE_TIMESTAMP}" to automatically generate the timestamp. '
      'Please double check the timezone of the operating system or container, so the correct timestamp is generated.',
  )

  @classmethod
  @override
  def execute(cls, timestamp: str) -> None:
    if timestamp == cls.AUTO_GENERATE_TIMESTAMP:
      timestamp = time.strftime(cls.TIME_FORMAT)
      logging.info(f'Using timestamp "{timestamp}".')

    Http.get('setsystime.cgi', {'time': timestamp})

  @staticmethod
  @override
  def flag_validator(timestamp: str | None) -> bool:
    if timestamp is None or timestamp == SetTimestamp.AUTO_GENERATE_TIMESTAMP:
      return True

    try:
      time.strptime(timestamp, SetTimestamp.TIME_FORMAT)
    except ValueError as e:
      raise flags.ValidationError(f'Timestamp validation failed with "{str(e)}".')

    return True
