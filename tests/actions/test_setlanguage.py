from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setlanguage import Language, SetLanguage
from m300_toolbox.http.http import Http


class TestSetLanguage(parameterized.TestCase):
  PARAMETERS = [{'language': language, 'value': language.value} for language in Language]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, language: Language, value: str):
    SetLanguage.execute(language)
    Http.get.assert_called_once_with('setlanguage.cgi', {'language': value})
    Http.get.reset_mock()
