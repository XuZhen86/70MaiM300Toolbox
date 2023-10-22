import builtins
import pprint  # from pprint import pprint doesn't work for @patch().
from unittest.mock import Mock, patch

from absl.testing import absltest, flagsaver
from jsonschema import ValidationError

from m300_toolbox.actions.sendcommandwithparams import SendCommandWithParams
from m300_toolbox.http.http import Http


class TestSendCommandWithParams(absltest.TestCase):

  @flagsaver.as_parsed((SendCommandWithParams.WITH_PARAMS, '{}'))
  @patch.object(Http, 'get', Mock())
  def test_noParams_sendsCommand(self):
    SendCommandWithParams.execute('command.cgi')
    Http.get.assert_called_once_with('command.cgi', {})

  @flagsaver.as_parsed((SendCommandWithParams.WITH_PARAMS, '{"key1":"1","key2":2}'))
  @patch.object(Http, 'get', Mock(return_value=None))
  def test_withParams_sendsCommandWithParams(self):
    result = SendCommandWithParams.execute('command.cgi')
    self.assertIsNone(result)
    Http.get.assert_called_once_with('command.cgi', {'key1': '1', 'key2': 2})

  @flagsaver.as_parsed((SendCommandWithParams.WITH_PARAMS, '{"key1":"1","key2":[]}'))
  @patch.object(Http, 'get', Mock())
  def test_invalidParamsValue_raises(self):
    with self.assertRaises(ValidationError):
      SendCommandWithParams.execute('command.cgi')
    Http.get.assert_not_called()
