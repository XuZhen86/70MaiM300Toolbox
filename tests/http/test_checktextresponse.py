from absl.testing import absltest

from m300_toolbox.http import Http


class TestCheckTextResponse(absltest.TestCase):
  COMMAND = 'command.cgi'
  PARAMS = {'str_param_1': '1', 'str_param_2': '2'}

  def test_emptyTextResponse_raises(self):
    with self.assertRaises(Exception):
      Http.check_text_response(self.COMMAND, self.PARAMS, '')

  def test_nonEmptyTextResponse_doesNotRaise(self):
    Http.check_text_response(self.COMMAND, self.PARAMS, 'non-empty')
