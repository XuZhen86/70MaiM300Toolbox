import pprint  # from pprint import pprint doesn't work for @patch().
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, final

from absl import flags

FlagValueT = TypeVar('FlagValueT')
ReturnValueT = TypeVar('ReturnValueT')


class Action(ABC, Generic[FlagValueT, ReturnValueT]):
  FLAG: flags.FlagHolder[FlagValueT | None]

  PRETTY_PRINT_RESULT = flags.DEFINE_boolean(
      name='pretty_print_result',
      default=True,
      help='Print the result with pprint() instead of print().',
  )

  @classmethod
  @final
  def _execute_and_print(cls) -> None:
    if not cls.FLAG.present or cls.FLAG.value is None:
      return

    return_value = cls.execute(cls.FLAG.value)
    if return_value is None:
      return

    if cls.PRETTY_PRINT_RESULT.value:
      pprint.pprint(return_value)
    else:
      print(return_value)

  @classmethod
  @abstractmethod
  def execute(cls, input_value: FlagValueT) -> ReturnValueT:
    raise NotImplementedError()

  @staticmethod
  def flag_validator(_: FlagValueT | None) -> bool:
    return True  # Not all Actions need to check flag. E.g. boolean and enum flags.
