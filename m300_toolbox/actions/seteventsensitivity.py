from enum import IntEnum, unique
from typing import override

from absl import flags

from m300_toolbox.actions.action import Action
from m300_toolbox.http import Http


@unique
class EventSensitivity(IntEnum):
  OFF = 0
  LOW = 1
  MID = 2
  HIGH = 3


class SetEventSensitivity(Action[EventSensitivity, None]):
  FLAG = flags.DEFINE_enum_class(
      name='set_event_sensitivity',
      default=None,
      enum_class=EventSensitivity,
      help='Sets the acceleration sensitivity for an event recording to start. '
      'This feature is usually advertized as "Collision Recording", '
      'based on the assumption that significant acceleration can be measured during a collision. '
      'High sensitivity means a mild acceleration would trigger the event. '
      'The videos are saved to the Event folder and will not be overwritten.',
  )

  @classmethod
  @override
  def execute(cls, sensitivity: EventSensitivity) -> None:
    Http.get('setcollision.cgi', {'level': int(sensitivity)})
