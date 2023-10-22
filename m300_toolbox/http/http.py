import hashlib
import json
import time
from typing import Callable

import jsonschema
import requests
from absl import flags
from requests.models import CaseInsensitiveDict


class Http:
  TOKEN = flags.DEFINE_string(
      name='token',
      default=None,
      required=True,
      help='A hex string of length 32 generated during the initial setup process. '
      'Use any random hex string of length 32 for the initial setup, and save the generated token for subsequent interactions. '
      'No API calls will be made if ',
  )

  HTTP_TIMEOUT_S = flags.DEFINE_float(
      name='http_timeout_s',
      default=120.0,
      lower_bound=10.0,
      help=
      'The dashcam can get stuck for a moment when processing a request and needs a longer HTTP timeout. '
      'It can also be helpful when the Wi-Fi connection is not stable.',
  )

  MAX_ATTEMPTS = flags.DEFINE_integer(
      name='max_attempts',
      default=3,
      lower_bound=1,
      help='Max times a request is attempted before raising an exception. '
      'A max_attempts of 3 means the request will be sent up to 3 times if it failed for HTTP issues. '
      'The request will not be retried if any response is received, even if the response is an error from the dashcam.',
  )

  @classmethod
  def get(cls,
          command: str,
          raw_params: dict[str, str | int] = {},
          text_response_fixer: Callable[[str], str] | None = None) -> dict | list | None:
    params = cls.sign_params(command, raw_params)
    text_response = cls.response(command, params).text  # Might use .json() here.
    cls.check_text_response(command, params, text_response)
    text_response = cls.apply_text_response_fixer(text_response, text_response_fixer)
    return cls.extract_result(text_response)

  @classmethod
  def sign_params(cls, command: str, raw_params: dict[str, str | int]) -> dict[str, str]:
    params = {'-' + key: str(value) for key, value in raw_params.items()}
    params['-timestamp'] = str(int(time.time()))
    params['-signkey'] = cls.signkey(command, params)
    return params

  @classmethod
  def response(cls, command: str, params: dict[str, str]) -> requests.Response:
    for _ in range(cls.MAX_ATTEMPTS.value):
      try:
        return requests.get(f'http://192.168.0.1/cgi-bin/{command}',
                            params=params,
                            timeout=cls.HTTP_TIMEOUT_S.value)
      except requests.Timeout:
        pass

    e = TimeoutError('Reached max number of attempts before a response could be obtained.')
    e.add_note(f'{command=}')
    e.add_note(f'{params=}')
    raise e

  @staticmethod
  def check_text_response(command: str, params: dict[str, str], text_response: str) -> None:
    if len(text_response) == 0:
      e = Exception('Text response is empty. Expected non-empty text response.')
      e.add_note(f'{command=}')
      e.add_note(f'{params=}')
      raise e

  @staticmethod
  def apply_text_response_fixer(text_response: str,
                                text_response_fixer: Callable[[str], str] | None) -> str:
    if text_response_fixer is not None:
      return text_response_fixer(text_response)
    return text_response

  @classmethod
  def signkey(cls, command: str, params: dict[str, str]) -> str:
    params_str = '&'.join(f'{key}={value}' for key, value in params.items())
    hash_str = command + '?' + params_str + cls.TOKEN.value
    return hashlib.md5(hash_str.encode()).hexdigest()

  TEXT_RESPONSE_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'object',
      'required': ['ResultCode'],
      'properties': {
          'ResultCode': {
              'type': 'string',
              'pattern': r'^0$',
              '$comment': 'Ensures the entire ResultCode string equals "0".'
          },
          'Result': {
              'type': ['object', 'array']
          }
      },
  })

  @classmethod
  def extract_result(cls, text_response: str) -> dict | list | None:
    try:
      json_response = json.loads(text_response)
    except json.JSONDecodeError as e:
      e.add_note(f'{text_response=}')
      raise

    cls.TEXT_RESPONSE_VALIDATOR.validate(json_response)
    return json_response.get('Result', None)

  @classmethod
  def headers(cls, url: str) -> CaseInsensitiveDict:
    for _ in range(cls.MAX_ATTEMPTS.value):
      try:
        return requests.head(url, timeout=cls.HTTP_TIMEOUT_S.value).headers
      except:
        pass

    e = Exception('Reached max number of attempts before a header could be obtained.')
    e.add_note(f'{url=}')
    raise e

  @classmethod
  def content(cls, url: str) -> bytes:
    for _ in range(cls.MAX_ATTEMPTS.value):
      try:
        # Might go Out of Memory.
        return requests.get(url, timeout=cls.HTTP_TIMEOUT_S.value).content
      except:
        pass

    e = Exception('Reached max number of attempts before a header could be obtained.')
    e.add_note(f'{url=}')
    raise e

  @staticmethod
  def flag_validator(token: str | None) -> bool:
    if token is None:
      return True

    if len(token) != 32:
      raise flags.ValidationError('Length of the token must be 32. '
                                  f'Got {len(token)} instead.')
    try:
      int(token, base=16)
    except Exception as e:
      raise flags.ValidationError('Unable to parse token as a hex string.') from e

    return True


flags.register_validator(Http.TOKEN, Http.flag_validator)
jsonschema.Draft202012Validator.check_schema(Http.TEXT_RESPONSE_VALIDATOR.schema)
