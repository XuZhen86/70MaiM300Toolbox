from unittest import TestCase
from unittest.mock import MagicMock, patch

from src.http import httputil
from src.misc import recordingutil


class TestRecordingUtil(TestCase):

  @patch('src.http.httputil.get_result', MagicMock(return_value=None))
  def test_start_recording(self):
    recordingutil.start_recording()
    httputil.get_result.assert_called_once_with('setaccessalbum.cgi', {'enable': 1})

  @patch('src.http.httputil.get_result', MagicMock(return_value=None))
  def test_stop_recording(self):
    recordingutil.stop_recording()
    httputil.get_result.assert_called_once_with('setaccessalbum.cgi', {'enable': 0})
