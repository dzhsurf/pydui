# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import Enum


class ButtonType(Enum):
    UNDEFINED = 0
    BUTTON_LEFT = 1
    BUTTON_RIGHT = 2


class ButtonEventType(Enum):
    UNDEFINED = 0
    PRESS = 1
    DBPRESS = 2
    TRIPRESS = 3
    RELEASE = 4


@dataclass(frozen=True)
class EventObject:
    pass


@dataclass(frozen=True)
class ButtonEvent(EventObject):
    x: int
    y: int
    button: ButtonType
    event: ButtonEventType
    time: int
