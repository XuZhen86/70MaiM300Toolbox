from unittest.mock import Mock

from absl.testing import absltest

from m300_toolbox.http import Http


class TestApplyTextResponseFixer(absltest.TestCase):
  TEXT_RESPONSE = 'text1 text2'
  FIXED_TEXT = 'text3'

  def test_noFixer_returnsUnmodified(self):
    text = Http.apply_text_response_fixer(self.TEXT_RESPONSE, None)
    self.assertEqual(text, self.TEXT_RESPONSE)

  def test_hasFixer_callsFixerAndReturnsText(self):
    text_response_fixer = Mock(return_value=self.FIXED_TEXT)

    text = Http.apply_text_response_fixer(self.TEXT_RESPONSE, text_response_fixer)

    self.assertEqual(text, self.FIXED_TEXT)
    text_response_fixer.assert_called_once_with(self.TEXT_RESPONSE)
