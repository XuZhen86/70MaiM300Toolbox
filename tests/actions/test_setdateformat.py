from unittest.mock import Mock, patch

from absl.testing import parameterized

from m300_toolbox.actions.setdateformat import DateFormat, SetDateFormat
from m300_toolbox.http.http import Http


class TestSetDateFormat(parameterized.TestCase):
  PARAMETERS = [{
      'date_format': date_format,
      'value': date_format.value
  } for date_format in DateFormat]

  @parameterized.parameters(*PARAMETERS)
  @patch.object(Http, 'get', Mock())
  def test_enum(self, date_format: DateFormat, value: int):
    SetDateFormat.execute(date_format)
    Http.get.assert_called_once_with('setdateformat.cgi', {'type': value})
    Http.get.reset_mock()
