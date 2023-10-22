from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.seteventsensitivity import EventSensitivity, SetEventSensitivity
from m300_toolbox.http.http import Http


class TestSetEventSensitivity(parameterized.TestCase):
  PARAMETERS = [{
      'sensitivity': sensitivity,
      'value': sensitivity.value
  } for sensitivity in EventSensitivity]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, sensitivity: EventSensitivity, value: int):
    SetEventSensitivity.execute(sensitivity)
    Http.get.assert_called_once_with('setcollision.cgi', {'level': value})
    Http.get.reset_mock()
