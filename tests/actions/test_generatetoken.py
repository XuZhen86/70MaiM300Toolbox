import json
import time
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from absl.testing import absltest, flagsaver
from jsonschema import ValidationError

from m300_toolbox.actions.generatetoken import GenerateToken
from m300_toolbox.http.http import Http


class TestGenerateToken(absltest.TestCase):
  SEED_TOKEN = '0' * 32
  SEED_TOKEN_PAIR_KEY = 'a019d19030a4a403660c873bf543fd6b'
  RESULT_TIMESTAMP = '1700000000'
  RESULT_TIMESTAMP_PAIR_KEY = 'bbbf6a64712098c543a59a4aad97bb3f'
  RESULT_TOKEN = '1' * 32
  TIMESTAMP = 1800000000.000000
  TIMESTAMP_SIGN_KEY = '974520addedcb676cbdba40cc8e85058'

  INVALID_BIND_BY_BANYA_RESULT = SimpleNamespace(text=json.dumps({
      'ResultCode': '0',
      'Result': {
          'invalid': 'result'
      }
  }))

  @flagsaver.as_parsed((Http.TOKEN, SEED_TOKEN))
  @patch.object(Http, 'response', Mock(return_value=INVALID_BIND_BY_BANYA_RESULT))
  def test_invalidBindByBanyaResult_raises(self):
    with self.assertRaises(ValidationError):
      GenerateToken.execute(True)
    Http.response.assert_called_once_with('BindByBanya.cgi', {
        '-usr': self.SEED_TOKEN,
        '-signkey': self.SEED_TOKEN_PAIR_KEY
    })

  VALID_BIND_BY_BANYA_RESULT = SimpleNamespace(text=json.dumps({
      'ResultCode': '0',
      'Result': {
          'Token': RESULT_TOKEN,
          'timestamp': RESULT_TIMESTAMP
      }
  }))
  INVALID_USER_CONFIRM_BY_BANYA_RESULT = SimpleNamespace(text=json.dumps({
      'ResultCode': '0',
      'Result': {
          'invalid': 'result'
      }
  }))

  @flagsaver.as_parsed((Http.TOKEN, SEED_TOKEN))
  @patch.object(
      Http, 'response',
      Mock(side_effect=[VALID_BIND_BY_BANYA_RESULT, INVALID_USER_CONFIRM_BY_BANYA_RESULT]))
  def test_invalidUserconfirmByBanyaResult_raises(self):
    with self.assertRaises(Exception):
      GenerateToken.execute(True)

    Http.response.assert_has_calls([
        call('BindByBanya.cgi', {
            '-usr': self.SEED_TOKEN,
            '-signkey': self.SEED_TOKEN_PAIR_KEY
        }),
        call('UserconfirmByBanya.cgi', {
            '-timestamp': self.RESULT_TIMESTAMP,
            '-signkey': self.RESULT_TIMESTAMP_PAIR_KEY
        })
    ])

  @flagsaver.as_parsed((Http.TOKEN, SEED_TOKEN))
  @patch.object(
      Http, 'response',
      Mock(side_effect=[
          VALID_BIND_BY_BANYA_RESULT,
          SimpleNamespace(text=json.dumps({'ResultCode': '0'})),
          SimpleNamespace(text=json.dumps({'ResultCode': '0'}))
      ]))
  @patch.object(time, 'time', Mock(return_value=TIMESTAMP))
  def test_goodResult_callsAndReturnsToken(self):
    token = GenerateToken.execute(True)

    self.assertEqual(token, self.RESULT_TOKEN)
    Http.response.assert_has_calls([
        call('BindByBanya.cgi', {
            '-usr': self.SEED_TOKEN,
            '-signkey': self.SEED_TOKEN_PAIR_KEY
        }),
        call('UserconfirmByBanya.cgi', {
            '-timestamp': self.RESULT_TIMESTAMP,
            '-signkey': self.RESULT_TIMESTAMP_PAIR_KEY
        }),
        call(
            'client.cgi', {
                '-operation': 'register',
                '-ip': '192.168.0.2',
                '-timestamp': str(int(self.TIMESTAMP)),
                '-signkey': '5948bb0d7c7ab2fb3715902b76e79d86'
            })
    ])
