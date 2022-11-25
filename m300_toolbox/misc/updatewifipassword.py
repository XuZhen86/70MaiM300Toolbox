import random
import string

from absl import logging

from m300_toolbox.http import httputil


def update_wifi_password() -> None:
  password = ''.join(random.choices(string.ascii_letters + string.digits, k=63))
  httputil.get_result('setwifi.cgi', {'wifikey': password})
  logging.info('password = %s', password)
  print('new wi-fi password: {}'.format(password))
