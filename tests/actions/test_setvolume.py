from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setvolume import SetVolume, Volume
from m300_toolbox.http.http import Http


class TestSetLanguage(parameterized.TestCase):
  PARAMETERS = [{'volume': volume, 'value': volume.value} for volume in Volume]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, volume: Volume, value: str):
    SetVolume.execute(volume)
    Http.get.assert_called_once_with('setaudiooutvolume.cgi', {'level': value})
    Http.get.reset_mock()
