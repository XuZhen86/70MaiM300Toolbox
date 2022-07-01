from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.sdcard import sdcardutil

_HTTPUTIL_GET_RESULT_MAGIC_MOCK = MagicMock(return_value={
    'sdstate': 'SDOK',
    'sdtotal': '122081MB',
    'sdused': '27159MB'
})


class TestGetSdCardStatus(TestCase):

  @patch('src.http.httputil.get_result', _HTTPUTIL_GET_RESULT_MAGIC_MOCK)
  @patch('builtins.print', MagicMock(return_value=None))
  def test(self):
    sd_card_status = sdcardutil.get_sd_card_status()

    self.assertEqual(sd_card_status.status, 'SDOK')
    self.assertEqual(sd_card_status.capacity_mb, 122081)
    self.assertEqual(sd_card_status.used_mb, 27159)
    print.assert_called_once_with(f'status: SDOK, capacity: 122081MB, used: 27159MB')
