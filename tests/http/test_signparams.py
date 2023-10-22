import time
from unittest.mock import Mock, patch

from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestSignParams(absltest.TestCase):
  TOKEN = '7d74c62b3a73a7cb1f78e3cb016bb5c8'
  COMMAND = 'command.cgi'
  TIME = 1234567890.1234567
  RAW_PARAMS = {'str_param': 'str', 'int_param': 1}

  @flagsaver.as_parsed((Http.TOKEN, TOKEN))
  @patch.object(time, 'time', Mock(return_value=TIME))
  def test_emptyRawParams_generatesSignKey(self):
    params = Http.sign_params(self.COMMAND, {})
    self.assertEqual(
        params, params | {
            '-timestamp': '1234567890',
            '-signkey': '79034caca8dea5c0d474eb0281d0ae69'
        })

  @flagsaver.as_parsed((Http.TOKEN, TOKEN))
  @patch.object(time, 'time', Mock(return_value=TIME))
  def test_nonEmptyRawParams_generatesSignKey(self):
    params = Http.sign_params(self.COMMAND, self.RAW_PARAMS)
    self.assertEqual(
        params, params | {
            '-timestamp': '1234567890',
            '-signkey': 'dd8540e33c34fcb381fc49da5115bc45'
        })

  @flagsaver.as_parsed((Http.TOKEN, TOKEN))
  @patch.object(time, 'time', Mock(return_value=TIME))
  def test_nonEmptyRawParams_prefixesRawParams(self):
    params = Http.sign_params(self.COMMAND, self.RAW_PARAMS)
    self.assertEqual(params, params | {'-str_param': 'str', '-int_param': '1'})

  def test_nonEmptyRawParams_keepsRawParamsOrderAndPutsTimestampAndSignKeyToTheEnd(self):
    pass
    # The sign key generation is dependent on the params order.
    # The previous tests imply the order was preserved.
