from unittest import TestCase
from unittest.mock import MagicMock, patch

from m300_toolbox.http import httputil
from m300_toolbox.sdcard import sdcardutil
from m300_toolbox.sdcard.sdcardstatus import SdCardStatus


class TestGetSdCardStatus(TestCase):

  def test_parses_from_result(self) -> None:
    sd_card_status = SdCardStatus({'sdstate': 'SDOK', 'sdtotal': '60882MB', 'sdused': '3360MB'})
    self.assertEqual(sd_card_status.status, 'SDOK')
    self.assertEqual(sd_card_status.capacity_mb, 60882)
    self.assertEqual(sd_card_status.used_mb, 3360)

  def test_missing_key_raises_key_error(self) -> None:
    with self.assertRaises(KeyError):
      SdCardStatus({})

  def test_result_field_does_not_ends_with_mb_raises_value_error(self) -> None:
    with self.assertRaises(ValueError):
      SdCardStatus({'sdstate': 'SDOK', 'sdtotal': '60882MBAAA', 'sdused': '3360MB'})

  def test_result_field_missing_mb_raises_value_error(self) -> None:
    with self.assertRaises(ValueError):
      SdCardStatus({'sdstate': 'SDOK', 'sdtotal': '60882', 'sdused': '3360MB'})


class TestFormatSdCard(TestCase):

  @patch('m300_toolbox.http.httputil.get_result', MagicMock(return_value=None))
  def test(self) -> None:
    sdcardutil.format_sd_card()

    httputil.get_result.assert_called_once_with('sdcommand.cgi', {'format': 1})
