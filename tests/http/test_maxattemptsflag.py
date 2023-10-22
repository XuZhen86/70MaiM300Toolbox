from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestMaxAttemptsFlag(absltest.TestCase):
  GOOD_MAX_ATTEMPTS = 5
  LOW_MAX_ATTEMPTS = 0

  def test_goodMaxAttempts_doesNotRaise(self):
    with flagsaver.as_parsed((Http.MAX_ATTEMPTS, str(self.GOOD_MAX_ATTEMPTS))):
      pass

  def test_lowMaxAttempts_raisesException(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((Http.MAX_ATTEMPTS, str(self.LOW_MAX_ATTEMPTS))):
        pass
