from enum import IntEnum
from typing import List


class FileType(IntEnum):
  NORMAL = 0
  UNKNOWN_TYPE_1 = 1
  PARKING = 2
  UNKNOWN_TYPE_3 = 3
  UNKNOWN_TYPE_4 = 4
  TIME_LAPSE = 5  # result.type == 4

  def get_local_path(self) -> str:
    match self.value:
      case FileType.NORMAL:
        return 'Normal'
      case FileType.PARKING:
        return 'Parking'
      case FileType.TIME_LAPSE:
        return 'TimeLapse'
      case _:
        raise NotImplementedError('local path for this FileType is not yet defined')

  @staticmethod
  def get_enabled_types() -> List:
    return [FileType.NORMAL, FileType.PARKING, FileType.TIME_LAPSE]
