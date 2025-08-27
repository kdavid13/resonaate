"""Defines a :class:`.Stardate` class to abstract an instant in time."""
from __future__ import annotations

from datetime import datetime
from enum import Enum


class DayFrac:
    """Number of elapsed days since _noon_ of January 1, 4713 BC."""

    def __init__(self, days_a: float, days_b: float = 0.0):
        """Instantiate a :class:`.DayFrac` instance from a two-part Julian day number.

        Args:
            days_a: Portion (or whole part) of Julian day number being represented.
            days_b: Portion (or whole part) of Julian day number being represented.
        """
        self._days_a = days_a
        self._days_b = days_b

    @property
    def days(self) -> float:
        """Returns the sum of the specified two-part Julian day number."""
        return self._days_a + self._days_b


class DatetimeExt:
    """Extended functionality encapsulated with a Python `datetime`."""

    def __init__(self, dt: datetime):
        """Instantiate a :class:`.DatetimeExt` from specified `datetime`.

        Args:
            dt: Specified Python `datetime` object.
        """
        self._dt = dt


class SecDelta:
    """Number of seconds since specified origin."""

    def __init__(self, sec: float, origin: Stardate):
        """Instantiate a :class:`.SecDelta` instance.

        Args:
            sec: Number of seconds that have passed since `origin`.
            origin: Specified instant in time to measure `sec` from.

        Todo:
            Would be nice to have an elegant way to generate an analagous `ScenarioTime` without
            needing to specify the origin...
        """
        self._sec = sec
        self._origin = origin


class TimeScale(Enum):
    """Enumeration of supported time scales."""

    TAI = "TAI"
    """International Atomic Time"""

    UT1 = "UT1"
    """Universal Time"""

    UTC = "UTC"
    """Coordinated Universal Time"""

    TT = "TT"
    """Terrestrial Time"""


class Stardate:
    """Abstracts an instant in time."""

    def __init__(self, time_val: DayFrac | SecDelta | datetime, scale: TimeScale):
        """Instantiate a :class:`.Stardate`.

        Args:
            time_val: The value of time being represented.
            scale: The scale of the `time_val`. Not all seconds are equal!
        """
        self._time_val = time_val
        if isinstance(self._time_val, datetime):
            self._time_val = DatetimeExt(self._time_val)
        self._scale = scale
