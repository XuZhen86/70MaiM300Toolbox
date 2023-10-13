from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests

from m300_toolbox.http.httputil import (_get_http_response, get_content_iterator, get_http_headers,
                                        get_result)

_HTTP_TIMEOUT_SEC = 30
_TIMESTAMP = 1000000000


@patch('time.time', MagicMock(return_value=_TIMESTAMP + 0.4))
@patch('m300_toolbox.http.httputil._CONNECT_KEY',
       SimpleNamespace(value='0123456789abcdef0123456789abcdef'))
@patch('m300_toolbox.http.httputil._HTTP_TIMEOUT_SEC', SimpleNamespace(value=_HTTP_TIMEOUT_SEC))
class TestGetHttpResponse(TestCase):

  @patch('requests.get', MagicMock(return_value=SimpleNamespace(text='{"ResultCode":"0"}')))
  def test_empty_params(self) -> None:
    response = _get_http_response('command.cgi')

    self.assertEqual(response.text, '{"ResultCode":"0"}')
    requests.get.assert_called_once_with('http://192.168.0.1/cgi-bin/command.cgi',
                                         params={
                                             '-timestamp': str(_TIMESTAMP),
                                             '-signkey': '8d4e78b2e534229e645ed2f0871d8f9b',
                                         },
                                         timeout=_HTTP_TIMEOUT_SEC)

  @patch('requests.get', MagicMock(return_value=SimpleNamespace(text='{"ResultCode":"0"}')))
  def test_nonempty_params(self) -> None:
    response = _get_http_response('command.cgi', {'intparams': 1111, 'stringparams': 'str'})

    self.assertEqual(response.text, '{"ResultCode":"0"}')
    requests.get.assert_called_once_with('http://192.168.0.1/cgi-bin/command.cgi',
                                         params={
                                             '-intparams': '1111',
                                             '-stringparams': 'str',
                                             '-timestamp': str(_TIMESTAMP),
                                             '-signkey': '572f565783f68c007a06c73f518a1dcf',
                                         },
                                         timeout=_HTTP_TIMEOUT_SEC)


class TestGetResult(TestCase):

  @patch('m300_toolbox.http.httputil._get_http_response',
         MagicMock(return_value=SimpleNamespace(text='')))
  def test_empty_text_response_raises_value_error(self) -> None:
    with self.assertRaises(ValueError):
      get_result('command.cgi', {})

  @patch('m300_toolbox.http.httputil._get_http_response',
         MagicMock(return_value=SimpleNamespace(text='{"ResultCode":"-6677"}')))
  def test_non_0_result_code_raises_value_error(self) -> None:
    with self.assertRaises(ValueError):
      get_result('command.cgi', {})

  @patch('m300_toolbox.http.httputil._get_http_response',
         MagicMock(return_value=SimpleNamespace(text='{"ResultCode":"0"}')))
  def test_empty_result(self) -> None:
    result = get_result('command.cgi', {})

    self.assertEqual(result, None)

  @patch(
      'm300_toolbox.http.httputil._get_http_response',
      MagicMock(return_value=SimpleNamespace(
          text='{"ResultCode":"0","Result":{"field1":"1","field2":"2"}}')))
  def test_nonempty_result(self) -> None:
    result = get_result('command.cgi', {})

    self.assertDictEqual(result, {'field1': '1', 'field2': '2'})

  @patch('m300_toolbox.http.httputil._get_http_response',
         MagicMock(return_value=SimpleNamespace(text='{"ResultCode":"0"}')))
  def test_text_response_preprocessor(self) -> None:
    text_response_preprocessor = MagicMock(return_value='{"ResultCode":"0"}')

    result = get_result('command.cgi', {}, text_response_preprocessor)

    self.assertEqual(result, None)
    text_response_preprocessor.assert_called_once_with('{"ResultCode":"0"}')


@patch('m300_toolbox.http.httputil._HTTP_TIMEOUT_SEC', SimpleNamespace(value=_HTTP_TIMEOUT_SEC))
class TestGetHttpHeaders(TestCase):

  @patch('requests.head',
         MagicMock(return_value=SimpleNamespace(headers={
             'key1': 'value1',
             'key2': 'value2'
         })))
  def test(self) -> None:
    headers = get_http_headers('http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4')

    self.assertDictEqual(headers, {'key1': 'value1', 'key2': 'value2'})
    requests.head.assert_called_once_with(
        'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4', timeout=_HTTP_TIMEOUT_SEC)


@patch('m300_toolbox.http.httputil._HTTP_TIMEOUT_SEC', SimpleNamespace(value=_HTTP_TIMEOUT_SEC))
class TestGetContentIterator(TestCase):

  @patch(
      'requests.get',
      MagicMock(return_value=SimpleNamespace(iter_content=MagicMock(return_value=[1, 2, 3, 4, 5]))))
  def test(self) -> None:
    content_iterator = get_content_iterator(
        'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4')

    self.assertListEqual(list(content_iterator), [1, 2, 3, 4, 5])
    requests.get.assert_called_once_with(
        'http://192.168.0.1/sd/Normal/NO20220610-121518-001121.mp4',
        timeout=_HTTP_TIMEOUT_SEC,
        stream=True)
    requests.get().iter_content.assert_called_once()
