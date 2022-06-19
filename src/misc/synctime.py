import datetime

from absl import logging
from src.http import httputil


def sync_time() -> None:
  formatted_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  httputil.get_result('setsystime.cgi', {'time': formatted_time})
  logging.info('synced to time %s', formatted_time)
