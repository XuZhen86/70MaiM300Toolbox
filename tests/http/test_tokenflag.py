from absl.flags import IllegalFlagValueError
from absl.testing import absltest, flagsaver

from m300_toolbox.http import Http


class TestTokenFlag(absltest.TestCase):
  GOOD_TOKEN = '7d74c62b3a73a7cb1f78e3cb016bb5c8'
  SHORT_TOKEN = '7d74c62b3a73a7cb1f78e3cb016bb5c'
  LONG_TOKEN = '7d74c62b3a73a7cb1f78e3cb016bb5c800'
  NON_HEX_TOKEN = '7g74g62g3a73a7cb1f78e3cb016bb5c'

  def test_goodToken_doesNotRaise(self):
    with flagsaver.as_parsed((Http.TOKEN, self.GOOD_TOKEN)):
      pass

  def test_shortToken_raisesException(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((Http.TOKEN, self.SHORT_TOKEN)):
        pass

  def test_longToken_raisesException(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((Http.TOKEN, self.SHORT_TOKEN)):
        pass

  def test_nonHexToken_raisesException(self):
    with self.assertRaises(IllegalFlagValueError):
      with flagsaver.as_parsed((Http.TOKEN, self.NON_HEX_TOKEN)):
        pass
