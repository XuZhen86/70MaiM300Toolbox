from unittest.mock import Mock, patch

from absl.testing import absltest
from jsonschema import ValidationError

from m300_toolbox.actions.getparkingwire import GetParkingWire
from m300_toolbox.http.http import Http


class TestGetParkingWire(absltest.TestCase):

  @patch.object(Http, 'get', Mock())
  def test_false_doNoting(self):
    GetParkingWire.execute(False)
    Http.get.assert_not_called()

  @patch.object(Http, 'get', Mock(return_value={'invalid': '0'}))
  def test_invalidKey_raises(self):
    with self.assertRaises(ValidationError):
      GetParkingWire.execute(True)
    Http.get.assert_called_once_with('getparkingwire.cgi')

  @patch.object(Http, 'get', Mock(return_value={'parkingwire': '2'}))
  def test_invalidValue_raises(self):
    with self.assertRaises(ValidationError):
      GetParkingWire.execute(True)
    Http.get.assert_called_once_with('getparkingwire.cgi')

  @patch.object(Http, 'get', Mock(return_value={'parkingwire': '1'}))
  def test_validResult_returns(self):
    result = GetParkingWire.execute(True)
    self.assertEqual(result, True)
    Http.get.assert_called_once_with('getparkingwire.cgi')
