from types import SimpleNamespace
from unittest.mock import Mock, patch

import requests
from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestContent(absltest.TestCase):
  HTTP_TIMEOUT_S = 12.34
  MAX_ATTEMPTS = 5
  URL = 'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4'
  GET_RETURN_VALUE = SimpleNamespace(content=b'1234')

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

  @patch.object(requests, 'get', Mock(side_effect=Exception()))
  def test_httpFails_makesMultipleAttemptsThenRaises(self):
    with self.assertRaises(Exception):
      Http.content(self.URL)

    self.assertLen(requests.get.mock_calls, self.MAX_ATTEMPTS)

  @patch.object(requests, 'get', Mock(return_value=GET_RETURN_VALUE))
  def test_httpSucceeds_callsHead(self):
    content = Http.content(self.URL)

    requests.get.assert_called_once_with(self.URL, timeout=self.HTTP_TIMEOUT_S)
    self.assertEqual(content, b'1234')
