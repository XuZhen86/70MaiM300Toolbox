from json import JSONDecodeError

from absl.testing import absltest
from jsonschema import ValidationError

from m300_toolbox.http import Http


class TestExtractResult(absltest.TestCase):

  def test_emptyString_raises(self):
    with self.assertRaises(JSONDecodeError):
      Http.extract_result('')

  def test_emptyObject_raises(self):
    with self.assertRaises(ValidationError):
      Http.extract_result('{}')

  def test_nonEmptyObject_raises(self):
    with self.assertRaises(ValidationError):
      Http.extract_result('{"A":"B"}')

  def test_resultCodeNot0_raises(self):
    with self.assertRaises(ValidationError):
      Http.extract_result('{"ResultCode":"-012"}')

  def test_missingResultCode_raises(self):
    with self.assertRaises(ValidationError):
      Http.extract_result('{"Result":{}}')

  def test_invalidResultType_raises(self):
    with self.assertRaises(ValidationError):
      Http.extract_result('{"ResultCode":"0","Result":"str"}')

  def test_resultCodeOnly_convertsToNone(self):
    result = Http.extract_result('{"ResultCode":"0"}')
    self.assertIsNone(result)

  def test_arrayResult_convertsToList(self):
    result = Http.extract_result('{"ResultCode":"0","Result":[]}')
    self.assertIsInstance(result, list)
    self.assertEmpty(result)

  def test_objectResult_convertsToDict(self):
    result = Http.extract_result('{"ResultCode":"0","Result":{}}')
    self.assertIsInstance(result, dict)
    self.assertEmpty(result)

  def test_extraProperties_ignored(self):
    result = Http.extract_result('{"ResultCode":"0","Result":{},"ExtraResult":[]}')
    self.assertIsInstance(result, dict)
    self.assertEmpty(result)
