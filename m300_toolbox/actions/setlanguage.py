from enum import StrEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class Language(StrEnum):
  ENGLISH = 'English'
  RUSSIAN = 'Русский'
  JAPANESE = '日本語'
  KOREAN = '한국어'
  SPANISH = 'Español'
  PORTUGUESE = 'Português'
  TRADITIONAL_CHINESE = '繁體中文'
  POLISH = 'Polski'
  THAI = 'ภาษาไทย'


class SetLanguage(Action[Language, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_language',
      default=None,
      enum_class=Language,
      help='Sets the language of the voice announcements. ',
  )

  @classmethod
  @override
  def execute(cls, language: Language) -> None:
    Http.get('setlanguage.cgi', {'language': str(language)})
