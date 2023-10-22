import hashlib
from typing import override

import jsonschema
from absl import flags
from absl.testing import flagsaver

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


class GenerateToken(Action[bool, str | None]):
  MAGIC_STRING = '73VpsAfdety8FDd0'

  FLAG = flags.DEFINE_boolean(
      name='generate_token',
      default=None,
      help='Does initial setup with the dashcam using any random token. '
      'The generated token is needed for all subsequent interactions.',
  )

  @classmethod
  @override
  def execute(cls, generate_token: bool) -> str | None:
    if not generate_token:
      return

    token, timestamp = cls._step_1(Http.TOKEN.value)
    cls._step_2(timestamp)
    with flagsaver.as_parsed((Http.TOKEN, token)):
      cls._step_3()

    return token

  STEP_1_VALIDATOR = jsonschema.Draft202012Validator({
      'type': 'object',
      'required': ['Token', 'timestamp'],
      'properties': {
          'Token': {
              'type': 'string',
              'pattern': r'^[0-9a-f]{32}$'
          },
          'timestamp': {
              'type': 'string',
              'pattern': r'^\d+$'
          }
      }
  })

  @classmethod
  def _pair_key(cls, payload: str) -> str:
    hash_str = payload + cls.MAGIC_STRING
    return hashlib.md5(hash_str.encode()).hexdigest()

  @classmethod
  def _step_1(cls, seed_token: str) -> tuple[str, str]:
    command = 'BindByBanya.cgi'
    params = {'-usr': seed_token, '-signkey': cls._pair_key(seed_token)}

    try:
      text_response = Http.response(command, params).text
      Http.check_text_response(command, params, text_response)
      result = Http.extract_result(text_response)

      cls.STEP_1_VALIDATOR.validate(result)
      assert isinstance(result, dict)

      return str(result['Token']), str(result['timestamp'])
    except Exception as e:
      e.add_note(f'{command=}')
      e.add_note(f'{params=}')
      raise

  @classmethod
  def _step_2(cls, timestamp: str) -> None:
    command = 'UserconfirmByBanya.cgi'
    params = {'-timestamp': timestamp, '-signkey': cls._pair_key(timestamp)}

    try:
      text_response = Http.response(command, params).text
      Http.check_text_response(command, params, text_response)
      result = Http.extract_result(text_response)
      assert result is None
    except Exception as e:
      e.add_note(f'{command=}')
      e.add_note(f'{params=}')
      raise

  @classmethod
  def _step_3(cls) -> None:
    result = Http.get('client.cgi', {'operation': 'register', 'ip': '192.168.0.2'})
    assert result is None


jsonschema.Draft202012Validator.check_schema(GenerateToken.STEP_1_VALIDATOR.schema)
