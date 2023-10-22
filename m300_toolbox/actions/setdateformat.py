from enum import IntEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class DateFormat(IntEnum):
  YYYYMMDD = 0
  DDMMYYYY = 1
  MMDDYYYY = 2


class SetDateFormat(Action[DateFormat, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_date_format',
      default=None,
      enum_class=DateFormat,
      help='Sets the format of the date in the video watermark. ',
  )

  @classmethod
  @override
  def execute(cls, format: DateFormat) -> None:
    Http.get('setdateformat.cgi', {'type': int(format)})
