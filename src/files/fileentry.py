from dataclasses import dataclass
from typing import Dict

from src.files.filetype import FileType


@dataclass
class FileEntry:

  path: str
  name: str
  size_b: int
  file_type: FileType

  # The size and type field in result are not accurate.
  # The caller should manuallly supply these fields.
  def __init__(self, result: Dict[str, str], size_b: int, file_type: FileType) -> None:
    self.path = result['path']
    self.name = result['name']
    self.size_b = size_b
    self.file_type = file_type

  # Compare based on timestamps only, ignores type.
  # If timestamp is the same, compare based on sequence number.
  def __lt__(self, other) -> bool:
    return self.name[2:] < other.name[2:]

  def get_local_path(self) -> str:
    file_type_path = self.file_type.get_local_path()
    date_path = self.name[2:-18]
    return f'{file_type_path}/{date_path}/{self.name}'


# Example results:
# [{"type":"0","count":"115"},{"type":"1","count":"0"},{"type":"2","count":"0"},{"type":"3","count":"0"},{"type":"4","count":"0"},{"type":"5","count":"132"},]
# {"path":"sd/Normal","name":"NO20220610-121418-001120.mp4","size":"125829120","type":"0"}
# {"path":"sd/Parking","name":"PA20211125-124504-000326.mp4","size":"125829120","type":"2"}
# {"path":"sd/Lapse","name":"LA20220610-224543-001143.mp4","size":"20971520","type":"4"}
