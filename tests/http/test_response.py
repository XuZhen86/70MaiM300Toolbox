from unittest.mock import Mock, patch

import requests
from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestResponse(absltest.TestCase):
  HTTP_TIMEOUT_S = 12.34
  MAX_ATTEMPTS = 5

  COMMAND = 'command.cgi'
  PARAMS = {'str_param_1': '1', 'str_param_2': '2'}

  def setUp(self) -> None:
    self.saved_flag_values = flagsaver.as_parsed(
        (Http.HTTP_TIMEOUT_S, str(self.HTTP_TIMEOUT_S)),
        (Http.MAX_ATTEMPTS, str(self.MAX_ATTEMPTS)),
    )
    self.saved_flag_values.__enter__()

    return super().setUp()

  def tearDown(self) -> None:
    self.saved_flag_values.__exit__(None, None, None)
    return super().tearDown()

  @patch.object(requests, 'get', Mock(side_effect=requests.Timeout()))
  def test_httpFails_makesMultipleAttemptsThenRaises(self):
    with self.assertRaises(TimeoutError):
      Http.response(self.COMMAND, self.PARAMS)

    self.assertLen(requests.get.mock_calls, self.MAX_ATTEMPTS)

  @patch.object(requests, 'get', Mock(return_value=requests.Response()))
  def test_httpSucceeds_callsGet(self):
    Http.response(self.COMMAND, self.PARAMS)

    requests.get.assert_called_once_with(f'http://192.168.0.1/cgi-bin/{self.COMMAND}',
                                         params=self.PARAMS,
                                         timeout=self.HTTP_TIMEOUT_S)
