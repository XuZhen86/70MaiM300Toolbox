from absl import logging
from src.http import httputil
from src.sdcard.sdcardstatus import SdCardStatus


def get_sd_card_status() -> None:
  result = httputil.get_result('getsdstate.cgi')
  sd_card_status = SdCardStatus(result)
  logging.info('%s', sd_card_status)
  return sd_card_status


def format_sd_card() -> None:
  httputil.get_result('sdcommand.cgi', {'format': 1})
