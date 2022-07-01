from absl import logging
from src.http import httputil
from src.sdcard.sdcardstatus import SdCardStatus


def get_sd_card_status() -> SdCardStatus:
  result = httputil.get_result('getsdstate.cgi')
  sd_card_status = SdCardStatus(result)
  logging.info('sd_card_status = %s', sd_card_status)
  print(
      f'status: {sd_card_status.status}, capacity: {sd_card_status.capacity_mb}MB, used: {sd_card_status.used_mb}MB'
  )
  return sd_card_status


def format_sd_card() -> None:
  httputil.get_result('sdcommand.cgi', {'format': 1})
