from unittest import TestCase
from unittest.mock import MagicMock, patch

from m300_toolbox.http import httputil
from m300_toolbox.misc import recordingutil


class TestRecordingUtil(TestCase):

  @patch('m300_toolbox.http.httputil.get_result', MagicMock(return_value=None))
  def test_start_recording(self) -> None:
    recordingutil.start_recording()
    httputil.get_result.assert_called_once_with('setaccessalbum.cgi', {'enable': 1})

  @patch('m300_toolbox.http.httputil.get_result', MagicMock(return_value=None))
  def test_stop_recording(self) -> None:
    recordingutil.stop_recording()
    httputil.get_result.assert_called_once_with('setaccessalbum.cgi', {'enable': 0})
