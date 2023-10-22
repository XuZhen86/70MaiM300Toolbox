import builtins
import pprint
from types import SimpleNamespace
from unittest.mock import Mock, patch

from absl.testing import absltest, flagsaver

from m300_toolbox.actions.action import Action


class TestAction(absltest.TestCase):

  def setUp(self):
    setattr(Action, 'FLAG', None)
    return super().setUp()

  def tearDown(self) -> None:
    delattr(Action, 'FLAG')
    return super().tearDown()

  @flagsaver.as_parsed((Action.PRETTY_PRINT_RESULT, 'false'))
  @patch.object(Action, 'FLAG', SimpleNamespace(present=False, value=None))
  @patch.object(Action, 'execute', Mock())
  def test_flagNotPresent_doesNotCallExecute(self):
    Action._execute_and_print()
    Action.execute.assert_not_called()

  @flagsaver.as_parsed((Action.PRETTY_PRINT_RESULT, 'false'))
  @patch.object(Action, 'FLAG', SimpleNamespace(present=True, value=None))
  @patch.object(Action, 'execute', Mock())
  def test_valueIsNone_doesNotCallExecute(self):
    Action._execute_and_print()
    Action.execute.assert_not_called()

  @flagsaver.as_parsed((Action.PRETTY_PRINT_RESULT, 'false'))
  @patch.object(Action, 'FLAG', SimpleNamespace(present=True, value=123))
  @patch.object(Action, 'execute', Mock(return_value=None))
  @patch.object(pprint, 'pprint', Mock())
  @patch.object(builtins, 'print', Mock())
  def test_valueIsPresent_callsExecuteWithFlagValue(self):
    Action._execute_and_print()
    Action.execute.assert_called_once_with(123)

  @flagsaver.as_parsed((Action.PRETTY_PRINT_RESULT, 'true'))
  @patch.object(Action, 'FLAG', SimpleNamespace(present=True, value=False))
  @patch.object(Action, 'execute', Mock(return_value=123))
  @patch.object(pprint, 'pprint', Mock())
  @patch.object(builtins, 'print', Mock())
  def test_executeReturnNotNoneAndPrettyPrint_callsPrint(self):
    Action._execute_and_print()
    Action.execute.assert_called_once_with(False)
    pprint.pprint.assert_called_once_with(123)
    print.assert_not_called()

  @flagsaver.as_parsed((Action.PRETTY_PRINT_RESULT, 'false'))
  @patch.object(Action, 'FLAG', SimpleNamespace(present=True, value=False))
  @patch.object(Action, 'execute', Mock(return_value=123))
  @patch.object(pprint, 'pprint', Mock())
  @patch.object(builtins, 'print', Mock())
  def test_executeReturnNotNoneAndNoPrettyPrint_callsPprint(self):
    Action._execute_and_print()
    Action.execute.assert_called_once_with(False)
    print.assert_called_once_with(123)
    pprint.pprint.assert_not_called()
