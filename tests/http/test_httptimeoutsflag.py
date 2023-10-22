from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestHttpTimeoutSFlag(absltest.TestCase):
  GOOD_TIMEOUT_S = 12.34
  SHORT_TIMEOUT_S = 1.23

  def test_goodTimeout_doesNotRaise(self):
    with flagsaver.as_parsed((Http.HTTP_TIMEOUT_S, str(self.GOOD_TIMEOUT_S))):
      pass

  def test_shortTimeout_raisesException(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((Http.HTTP_TIMEOUT_S, str(self.SHORT_TIMEOUT_S))):
        pass
