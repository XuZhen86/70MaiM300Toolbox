from dataclasses import dataclass
from typing import Dict


@dataclass
class SdCardStatus:
  status: str
  capacity_mb: int
  used_mb: int

  def __init__(self, result: Dict[str, str]) -> None:
    self.status = result['sdstate']
    self.capacity_mb = _parse_result_field_mb(result['sdtotal'])
    self.used_mb = _parse_result_field_mb(result['sdused'])


def _parse_result_field_mb(field: str) -> int:
  if not field.endswith('MB'):
    raise ValueError("field does not end with 'MB': " + field)
  return int(field[:-2])
