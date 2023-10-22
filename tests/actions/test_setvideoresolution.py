from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setvideoresolution import SetVideoResolution, VideoResolution
from m300_toolbox.http.http import Http


class TestSetLanguage(parameterized.TestCase):
  PARAMETERS = [{'res': res, 'value': res.value} for res in VideoResolution]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, res: VideoResolution, value: str):
    SetVideoResolution.execute(res)
    Http.get.assert_called_once_with('setparameter.cgi', {'workmode': 0, 'type': 0, 'value': value})
    Http.get.reset_mock()
