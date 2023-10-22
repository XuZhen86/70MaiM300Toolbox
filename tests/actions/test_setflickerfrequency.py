from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setflickerfrequency import FlickerFrequency, SetFlickerFrequency
from m300_toolbox.http.http import Http


class TestSetFlickerFrequency(parameterized.TestCase):
  PARAMETERS = [{
      'frequency': frequency,
      'value': frequency.value
  } for frequency in FlickerFrequency]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, frequency: FlickerFrequency, value: str):
    SetFlickerFrequency.execute(frequency)
    Http.get.assert_called_once_with('setp1n0.cgi', {'ntscpal': value})
    Http.get.reset_mock()
