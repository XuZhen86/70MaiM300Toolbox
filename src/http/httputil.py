import hashlib
import json
import time
from typing import Any, Callable, Dict, Iterator, Optional

import requests
from absl import flags, logging

_CONNECT_KEY = flags.DEFINE_string(
    name='connect_key',
    default=None,
    required=True,
    help='A 32 char long hex string generated when paring with the phone. '
    'It can either be found in 70mai app data, '
    'or use Wireshark to sniff clear text HTTP packages when pairing. '
    'Example: --connect_key=873ea99b5db1e67d1f065dedce6059f0')

_HTTP_TIMEOUT_SEC = flags.DEFINE_float(
    name='http_timeout_sec',
    default=30,
    required=False,
    help='Longer HTTP timeout in case the Wi-Fi connection is weak. '
    'Example: --http_timeout_sec=60')


def _process_raw_params(raw_params: Dict[str, Any] = {}) -> Dict[str, str]:
  params: Dict[str, str] = {}
  for key, value in raw_params.items():
    params['-' + key] = str(value)

  # -timestamp has to be the last param for some commands.
  params['-timestamp'] = str(int(time.time()))

  return params


def _generate_sign_key(command: str, params: Dict[str, str]) -> str:
  params_str = '&'.join(f'{key}={value}' for key, value in params.items())
  hash_str = f'{command}?{params_str}{_CONNECT_KEY.value}'
  sign_key = hashlib.md5(hash_str.encode('utf-8')).hexdigest()
  return sign_key


def _get_http_response(command: str, raw_params: Dict[str, Any] = {}) -> requests.Response:
  params = _process_raw_params(raw_params)
  sign_key = _generate_sign_key(command, params)
  params['-signkey'] = sign_key
  response = requests.get(f'http://192.168.0.1/cgi-bin/{command}',
                          params=params,
                          timeout=_HTTP_TIMEOUT_SEC.value)
  logging.debug('response.text = %s', response.text)
  return response


def get_result(command: str,
               raw_params: Dict[str, Any] = {},
               text_response_preprocessor: Optional[Callable[[str], str]] = None) -> Any:
  text_response = _get_http_response(command, raw_params).text
  if text_response_preprocessor is not None:
    text_response = text_response_preprocessor(text_response)

  if len(text_response) == 0:
    raise ValueError('response_text is empty')

  json_response: Dict[str, Any] = json.loads(text_response)
  result_code = int(json_response['ResultCode'])
  if result_code != 0:
    raise ValueError(f'result_code is {result_code}, expected 0')

  if 'Result' in json_response:
    return json_response['Result']

  return None


def get_http_headers(url: str) -> Dict[str, str]:
  return requests.head(url, timeout=_HTTP_TIMEOUT_SEC.value).headers


def get_content_iterator(url: str) -> Iterator:
  return requests.get(url, timeout=_HTTP_TIMEOUT_SEC.value,
                      stream=True).iter_content(1024**2)  # 1MiB
