from unittest.mock import Mock, patch

from absl.testing import absltest
from jsonschema import ValidationError

from m300_toolbox.actions.getsdcardstatus import GetSdCardStatus, SdCardStatus
from m300_toolbox.http.http import Http


class TestGetSdCardStatus(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_false_doNoting(self):
    GetSdCardStatus.execute(False)
    Http.get.assert_not_called()

  @patch.object(Http, 'get', Mock(return_value={'sdtotal': '0MB', 'sdused': '0MB'}))
  def test_missingKeys_raises(self):
    with self.assertRaises(ValidationError):
      GetSdCardStatus.execute(True)
    Http.get.assert_called_once_with('getsdstate.cgi')

  @patch.object(Http, 'get', Mock(return_value={
      'sdstate': 'state',
      'sdtotal': '0',
      'sdused': '0MB'
  }))
  def test_valueDoesNotEndWithMb_raises(self):
    with self.assertRaises(ValidationError):
      GetSdCardStatus.execute(True)
    Http.get.assert_called_once_with('getsdstate.cgi')

  @patch.object(Http, 'get',
                Mock(return_value={
                    'sdstate': 'state',
                    'sdtotal': 'MB',
                    'sdused': '0MB'
                }))
  def test_valueDoesNotStartWithNumber_raises(self):
    with self.assertRaises(ValidationError):
      GetSdCardStatus.execute(True)
    Http.get.assert_called_once_with('getsdstate.cgi')

  @patch.object(Http, 'get',
                Mock(return_value={
                    'sdstate': 'state',
                    'sdtotal': '1MB',
                    'sdused': '2MB'
                }))
  def test_validResult_returns(self):
    status = GetSdCardStatus.execute(True)
    self.assertEqual(status, SdCardStatus(state='state', capacity_mb=1, used_mb=2))
    Http.get.assert_called_once_with('getsdstate.cgi')
