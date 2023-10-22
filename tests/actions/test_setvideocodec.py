from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setvideocodec import SetVideoCodec, VideoCodec
from m300_toolbox.http.http import Http


class TestSetLanguage(parameterized.TestCase):
  PARAMETERS = [{'codec': codec, 'value': codec.value} for codec in VideoCodec]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, codec: VideoCodec, value: str):
    SetVideoCodec.execute(codec)
    Http.get.assert_called_once_with('setparameter.cgi', {
        'workmode': 0,
        'type': 0,
        'videoencode': value
    })
    Http.get.reset_mock()
